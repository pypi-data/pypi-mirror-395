from __future__ import annotations

import os, io, re, json, base64
from typing import Any, Dict, List, Optional

from syntaxmatrix import profiles as _prof
from syntaxmatrix.settings.model_map import GPT_MODELS_LATEST 
from syntaxmatrix.gpt_models_latest import extract_output_text as _out, set_args
from google.genai import types


# Axes/labels/legend (read-only; no plotting changes)
MPL_PROBE_SNIPPET = r"""
    import json
    import matplotlib.pyplot as plt

    out=[]
    for num in plt.get_fignums():
        fig = plt.figure(num)
        for ax in fig.get_axes():
            info = {
                "title": (ax.get_title() or "").strip(),
                "x_label": (ax.get_xlabel() or "").strip(),
                "y_label": (ax.get_ylabel() or "").strip(),
                "legend": []
            }
            try:
                leg = ax.get_legend()
                if leg:
                    info["legend"] = [t.get_text().strip() for t in leg.get_texts() if t.get_text().strip()]
            except Exception:
                pass
            out.append(info)
    print("SMX_VIS_SUMMARY::" + json.dumps(out))
"""

# 2) Figure images to base64 (tight bbox, high DPI)
MPL_IMAGE_PROBE_SNIPPET = r"""
    import json, io, base64
    import matplotlib.pyplot as plt

    payload=[]
    for num in plt.get_fignums():
        fig = plt.figure(num)
        axes=[]
        for ax in fig.get_axes():
            info={"title": (ax.get_title() or "").strip(),
                "x_label": (ax.get_xlabel() or "").strip(),
                "y_label": (ax.get_ylabel() or "").strip(),
                "legend": []}
            try:
                leg = ax.get_legend()
                if leg:
                    info["legend"] = [t.get_text().strip() for t in leg.get_texts() if t.get_text().strip()]
            except Exception:
                pass
            axes.append(info)

        b64 = ""
        try:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=192, bbox_inches="tight", facecolor="white")
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode("ascii")
        except Exception:
            b64 = ""
        payload.append({"png_b64": b64, "axes": axes})
    print("SMX_FIGS_B64::" + json.dumps(payload))
"""


def _json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), indent=2)


def parse_mpl_probe_output(text_blocks: List[str]) -> List[Dict[str, Any]]:
    joined = "\n".join(text_blocks)
    m = re.search(r"SMX_VIS_SUMMARY::(\[.*\]|\{.*\})", joined, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return data if isinstance(data, list) else []
    except Exception:
        return []
    
def parse_image_probe_output(text_blocks: List[str]) -> List[Dict[str, Any]]:
    joined = "\n".join(text_blocks)
    m = re.search(r"SMX_FIGS_B64::(\[.*\])", joined, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return data if isinstance(data, list) else []
    except Exception:
        return []

# 3) Table headers (from already-rendered HTML) — optional but helps context
def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s).strip()

def sniff_tables_from_html(html: str) -> List[Dict[str, Any]]:
    tables=[]
    for tbl in re.findall(r"<table[^>]*class=[\"'][^\"']*smx-table[^\"']*[\"'][^>]*>(.*?)</table>",
                          html, re.DOTALL|re.IGNORECASE):
        ths = re.findall(r"<th[^>]*>(.*?)</th>", tbl, re.DOTALL|re.IGNORECASE)
        headers = [_strip_tags(h) for h in ths][:50]
        trs = re.findall(r"<tr[^>]*>", tbl, re.IGNORECASE)
        tables.append({
            "columns": headers,
            "columns_count": len(headers),
            "rows_approx": max(0, len(trs)-1)
        })
    return tables


def build_display_summary(question: str,
                          mpl_axes: List[Dict[str, Any]],
                          html_blocks: List[str]) -> Dict[str, Any]:
    html_joined = "\n".join(str(b) for b in html_blocks)
    tables = sniff_tables_from_html(html_joined)

    axes_clean=[]
    for ax in mpl_axes:
        axes_clean.append({
            "title": ax.get("title",""),
            "x_label": ax.get("x_label",""),
            "y_label": ax.get("y_label",""),
            "legend": ax.get("legend", []),
        })

    return {
        "question": (question or "").strip(),
        "axes": axes_clean,
        "tables": tables
    }

def _context_strings(context: Dict[str, Any]) -> List[str]:
    s = [context.get("question","")]
    for ax in context.get("axes", []) or []:
        s += [ax.get("title",""), ax.get("x_label",""), ax.get("y_label","")]
        s += (ax.get("legend", []) or [])
    for t in context.get("tables", []) or []:
        s += (t.get("columns", []) or [])
    # de-dup
    seen=set(); out=[]
    for it in s:
        it=(it or "").strip()
        if not it: continue
        k=it.lower()
        if k in seen: continue
        seen.add(k); out.append(it)
    return out


def phrase_commentary_vision(context: Dict[str, Any], images_b64: List[str]) -> str:
    """
    Use the project's 'vision2text' profile (profiles.py). If the provider supports images,
    send figures + text; otherwise fall back to a text-only prompt grounded by labels.
    """
    
    _SYSTEM_VISION = (
        "You are a data analyst. Write a detailed analysis that explains what the "
        "already-rendered visuals mean for the user's question. "
        "You use information visible in the attached figures and the provided context strings (texs, field names, labels). "
        "You interprete the output without preamble."
    )

    _USER_TMPL_VISION = """
    question:
    {q}

    Visible context strings (titles, axes, legends, headers):
    {ctx}

    Write a comprehensive conclusion (~250-350 words) as follows:
    - <b>Headline</b> 
      2-3 sentence answering the question from an overview of all the output.
    - <b>Evidence</b> 
      8-10 bullets referencing the (output-texts/tables/panels/axes/legend groups) seen in the output. 
      As you reference the visuals, you should interprete them in a way to show how they answer the question.
    - <b>Limitations</b> 
      1 bullet; avoid quoting numbers unless present in context.
    - <b>Next step</b> 
      1 bullet.
    """

    visible = _context_strings(context)
    user = _USER_TMPL_VISION.format(
        q=context.get("question",""),
        ctx=json.dumps(visible, ensure_ascii=False, indent=2)
    )
     
    prof = _prof.get_profile("vision2text") or _prof.get_profile("admin")
    if not prof:    
        return (
            "<div class='smx-alert smx-alert-warn'>"
                "No LLM profile is configured for Image2Text. Please, do that in the Admin panel or contact your Administrator."
            "</div>"
        )
    
    prof['client'] = _prof.get_client(prof)
    _client = prof["client"]
    _provider = prof["provider"].lower()
    _model = prof["model"]

    try:
        #1 Google
        if _provider == "google":
            try:
                input_contents = []
                
                # Add text part first
                text_part = {"text": user}
                input_contents.append(text_part)
                
                # Add image parts
                for b64 in images_b64:
                    if b64:
                        image_part = {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": b64
                            }
                        }
                        input_contents.append(image_part)
                
                response = _client.models.generate_content(
                    model=_model,
                    contents=input_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=_SYSTEM_VISION,
                        temperature=0.7,
                        max_output_tokens=1024,
                    ),
                )
                txt = response.text.strip()
                return txt.strip()
            except Exception:
                pass
            
        #2 Openai
        elif _provider == "openai" and _model in GPT_MODELS_LATEST:
            try:
                input_contents = []

                text_part = {"type": "input_text", "text": user}
                input_contents.append(text_part)
                for b64 in images_b64:
                    if b64:
                        image_part = {
                            "type": "input_image", 
                            "image_url": f"data:image/png;base64,{b64}"
                        }
                        input_contents.append(image_part)

                args = set_args(
                    model=_model,
                    instructions=_SYSTEM_VISION,
                    input=[{"role": "user", "content": input_contents}],
                    previous_id=None,
                    store=False,
                    reasoning_effort="low",
                    verbosity="medium",
                )
                resp = _client.responses.create(**args)
                txt = _out(resp) or ""
                if txt.strip():
                    return txt.strip()
            except Exception:
                pass 
                    
        # Anthropic
        elif _provider == "anthropic":
            try:
                input_contents = []

                text_part = {"type":"text","text": user}
                input_contents.append(text_part)

                for b64 in images_b64:
                    if b64:
                        image_part = {
                            "type":"image_url",
                            "image_url":{"url": f"data:image/png;base64,{b64}"}
                        }
                        input_contents.append(image_part)       

                response = _client.messages.create(
                    model=_model,
                    max_tokens=1024,
                    system=_SYSTEM_VISION,
                    messages=[{"role": "user", "content":input_contents}],
                    stream=False,
                )
                return response.content[0].text.strip()   
            except Exception:
                pass 
        
        # OpenAI SDK
        else: 
            try:
                input_contents = [{"type":"text","text": user}]
                for b64 in images_b64:
                    if b64:
                        input_contents.append({"type":"image_url","image_url":{"url": f"data:image/png;base64,{b64}"}})
                resp = _client.chat.completions.create(
                    model=_model,
                    temperature=1,
                    messages=[
                        {"role":"system","content":_SYSTEM_VISION},
                        {"role":"user","content":input_contents},
                    ],
                    max_tokens=1024,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception:
                pass
    except Exception:
        return "Insufficient context to comment usefully."

def wrap_html(card_text: str) -> str:
    return f"""
        <div class="smx-commentary-card" style="margin-top:1rem;padding:1rem;border:1px solid #e5e7eb;border-radius:0.75rem;background:#fafafa">
        <div style="font-weight:600;margin-bottom:0.5rem;">smxAI Feedback</div>
        <div class="prose" style="white-space:pre-wrap;line-height:1.45">{card_text}</div>
        </div>
    """.strip()
