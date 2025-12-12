

# SyntaxMatrix — Developer Guide
---

## Overview

SyntaxMatrix focuses your app code on **logic** while it handles the chat UI, session state, file uploads, embeddings, and retrieval over two memories: **SMIV** (user uploads; per-session) and **SMPV** (system/company docs; persistent).

- Session-aware chat history
- Hybrid retrieval (user + system), or user-only, system-only, or none
- Streaming and non‑streaming modes
- Simple feature toggles in `settings.py`
- Branding and site controls (logo, favicon, titles), theme + UI mode switches
- Widgets (text input, buttons, dropdowns, uploader) and simple layout helpers

---

## Installation

```bash
pip install syntaxmatrix syntaxmatrix[mlearning,auth]
```

> Make sure your environment has any required API keys (e.g. OpenAI SDK compatible) available to your app.

---

## Quick start

**settings.py** — feature flags & branding in one place
```python
from syntaxmatrix import (
    enable_user_files, enable_stream, set_theme,
    set_site_logo, set_site_title, set_project_name, set_favicon, set_user_icon,
)

enable_user_files()
enable_stream()
set_theme('light')  # available: light, dark, chark, github, solarized-light, solarized-dark, oceanic-next, ayu-mirage, one-dark

# Branding (examples)
set_site_logo("<img src='/static/logo.svg' style='height:22px;vertical-align:middle'>")
set_site_title("SyntaxMatrix Demo")
set_project_name("SyntaxMatrix Demo")  # used in nav & metadata
set_favicon("<link rel='icon' href='/static/favicon.ico'>")
set_user_icon("👤")
```

**app.py** — minimal consumer app
```python
import syntaxmatrix as smx
from settings import *

def create_conversation(stream=False):
    chat = smx.get_chat_history() or []
    sid = smx.get_session_id()
    index = smx.smiv_index(sid)

    query, intent = smx.get_text_input_value("user_query")
    if not query: return
    query = query.strip()
    chat.append(("User", query))

    # Retrieval (optional)
    if intent == "none":
        context, sources = "", []
    else:
        vec = smx.embed_query(query)
        if vec is None: return
        ctx, sources = [], []
        if intent in ["hybrid","user_docs"]:
            hits = index.search(vec, top_k=3) or []
            ctx += ["\n### Personal Context (user uploads)\n"] + [f"- {{h['metadata']['chunk_text'].strip().replace('\\n',' ')}}\n" for h in hits]
            if hits: sources.append("User Docs")
        if intent in ["hybrid","system_docs"]:
            sys = smx.smpv_search(vec, top_k=5) or []
            if not sys: smx.error("Please contact support."); return
            ctx += ["### System Context (company docs)\n"] + [f"- {{h['chunk_text'].strip().replace('\\n',' ')}}\n" for h in sys]
            sources.append("System Docs")
        context = "".join(ctx)

    transcript = "\n".join([f"{{r}}: {{m}}" for r,m in chat])

    if stream:
        smx.stream_process_query(query, context, transcript, sources)
    else:
        ans = smx.process_query(query, context, transcript)
        if isinstance(ans, str) and ans.strip():
            if sources:
                ans += "".join([f"<ul style='margin-top:5px;color:blue;font-size:0.8rem;'><li>{{s}}</li></ul>" for s in sources])
            chat.append(("Bot", ans))

    smx.set_chat_history(chat)
    smx.clear_text_input_value("user_query")

# UI widgets
smx.text_input("user_query", "user_query", "Enter query", "Ask anything .")
smx.button("submit_query","submit_query","Submit", lambda: create_conversation(smx.stream()))
smx.file_uploader("user_files","user_files","Upload PDF files:", accept_multiple_files=True)

def clear_chat(): smx.clear_chat_history()
smx.button("clear_chat","clear_chat","Clear", clear_chat, stream=False)

if __name__ == "__main__":
    smx.run()
```

---

## Full API surface (open-source)

### App, theme, and UI
```python
smx.run()                                 # start the app
smx.set_ui_mode(mode)                     # one of: default, bubble, card, smx
smx.get_ui_modes()                        # → list of modes
smx.set_theme(name)                       # one of: light, dark, chark, github, solarized-light, solarized-dark, oceanic-next, ayu-mirage, one-dark
smx.get_themes()                          # → dict(name → colours)
smx.enable_theme_toggle()                 # adds theme toggle to navbar
smx.enable_user_files()                   # enables PDF uploader + SMIV
smx.enable_stream()                       # enable streaming mode globally
smx.stream()                              # returns True/False at runtime
```

### Branding & site identity
```python
smx.set_site_logo(html)                   # e.g. "<img src='/static/logo.svg' ...>"
smx.set_site_title("Your Site Title")     # text next to the logo in navbar
smx.set_project_name("Your Project")      # used in nav/meta contexts
smx.set_favicon("<link rel='icon' href='/static/favicon.ico'>")  # raw <link> tag
smx.set_user_icon("🙂")                    # icon used for user bubbles
smx.set_website_description(text)         # used by /about and SEO meta
```

**Notes**
- `set_site_logo` accepts **HTML** (so you can style the `<img>` inline).
- `set_favicon` expects the full `<link ...>` element; store your icon in `/static/` and reference it there.

### Widgets & layout
```python
smx.text_input(key, id, label, placeholder)       # register a text box
text, intent = smx.get_text_input_value(id)       # returns (string, intent)

smx.button(key, id, label, callback, stream=False)
smx.clear_text_input_value(id)

smx.file_uploader(key, id, label, accept_multiple_files=True)
files = smx.get_file_upload_value(id)             # list-like (optional use)

smx.dropdown(key, options, label=None, callback=None)
value = smx.get_widget_value(key)                 # read current selection

html = smx.columns([left_html, right_html])       # simple two+ column layout
```

### Sessions & history
```python
sid = smx.get_session_id()
hist = smx.get_chat_history()
smx.set_chat_history(hist or [])
smx.clear_chat_history()
```

### Retrieval & embeddings
```python
vec = smx.embed_query(query)                      # → embedding vector
idx = smx.smiv_index(sid)                         # session index (SMIV)
hits = idx.search(vec, top_k=3)                   # user uploads
sys_hits = smx.smpv_search(vec, top_k=5)          # system/company docs

# Pre-load system PDFs (optional, e.g. on startup)
smx.load_sys_chunks("uploads/sys")                # populates in-memory cache
```

### Answering (streaming & non-streaming)
```python
smx.stream_process_query(query, context, conversations, sources)
smx.process_query(query, context, conversations)  # → str
smx.process_query_stream(query, context, conversations)  # alt helper
smx.get_stream_args()                             # read any stream args (advanced)
```

### Prompt & profile helpers
```python
smx.set_prompt_profile(purpose="chat", profile_name="default")  # select profile
smx.set_prompt_instructions("You are ...")                      # set system text

# Embed model record (provider/model/key) stored encrypted in local DB:
smx.save_embed_model(provider="openai", model="gpt-5-mini", api_key="sk-...")
cfg = smx.load_embed_model()                                    # → dict
smx.delete_embed_key()                                          # wipe stored key
```

> Behind the scenes, profiles/keys live in a local SQLite DB (encrypted API key via Fernet).

### Advanced: Flask app access
```python
app = smx.app                         # access underlying Flask app
@app.route("/docs")
def docs_alias():
    from flask import redirect, url_for
    return redirect(url_for('view_page', page_name='docs'))
```

---

## Theming and UI modes

- **Themes:** light, dark, chark, github, solarized-light, solarized-dark, oceanic-next, ayu-mirage, one-dark
  ```python
  smx.set_theme('github')
  smx.enable_theme_toggle()
  ```

- **UI modes:** default, bubble, card, smx
  ```python
  smx.set_ui_mode('bubble')  # try 'card' for boxy chat, or 'smx' for framework default
  ```

---

<!-- ## Professional Docs page (Shadow DOM)

Paste this into **/admin → Edit Page → docs**. It renders `/static/docs.md` inside a Shadow DOM with its own CSS, so global CSS can’t distort it.

```html
<div id="syntaxmatrix-docs-root"></div>
<script>
(function () {{
  const host = document.getElementById('syntaxmatrix-docs-root');
  const shadow = host.attachShadow({{ mode: 'open' }});
  shadow.innerHTML = `
    <style>
      :host {{ all: initial; }}
      .doc {{ box-sizing:border-box; max-width: 980px; margin: 0 auto; padding: 24px;
              color:#1b1f23; background:#fff; font: 16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Helvetica,Arial,Noto Sans,sans-serif; }}
      .doc * {{ box-sizing: inherit; text-align: left; }}
      .doc h1 {{ font-size: 2rem; margin: 0 0 .75rem }}
      .doc h2 {{ margin-top: 2rem; padding-bottom: .4rem; border-bottom: 1px solid #e1e4e8; }}
      .doc h3 {{ margin-top: 1.25rem; }}
      .doc p, .doc li {{ line-height: 1.65; }}
      .doc ul, .doc ol {{ padding-left: 24px; }}
      .doc blockquote {{ border-left: 4px solid #e1e4e8; margin: 1rem 0; padding: .25rem 1rem; color: #586069; background: #fafbfc; }}
      .doc code, .doc pre {{ font-family: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono','Courier New',monospace; }}
      .doc pre {{ white-space: pre; background:#f6f8fa; border:1px solid #e1e4e8; padding:12px; border-radius:8px; overflow:auto; position: relative; }}
      .copy-btn {{ position:absolute; top:8px; right:8px; border:1px solid #e1e4e8; background:#fff; padding:2px 8px; border-radius:6px; font-size:.8rem; cursor:pointer; }}
      .doc table {{ border-collapse: collapse; width: 100%; }}
      .doc th, .doc td {{ border:1px solid #e1e4e8; padding:6px 10px; vertical-align: top; }}
      .doc img {{ max-width:100%; height:auto; }}
      .doc .note {{ background:#f6f8fa; border:1px solid #e1e4e8; padding:10px 12px; border-radius:8px; }}
    </style>
    <article class="doc"><p class="note">Loading documentation…</p></article>
  `;
  const container = shadow.querySelector('.doc');
  const mk = document.createElement('script');
  mk.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
  mk.onload = () => {{ fetch('/static/docs.md', {{ cache: 'no-cache' }}) 
    .then(r => r.text())
    .then(md => {{ container.innerHTML = window.marked.parse(md); addCopyButtons(); }})
    .catch(() => {{ container.innerHTML = '<p style="color:#b00">Could not load <code>static/docs.md</code>.</p>'; }}); }};
  shadow.appendChild(mk);
  function addCopyButtons() {{ shadow.querySelectorAll('pre > code').forEach(code => {{
    const btn = document.createElement('button'); btn.className = 'copy-btn'; btn.textContent = 'Copy';
    btn.addEventListener('click', () => {{ navigator.clipboard.writeText(code.textContent || ''); btn.textContent = 'Copied'; setTimeout(() => btn.textContent='Copy', 900); }});
    code.parentElement.appendChild(btn);
  }}); }}
}})();
</script>
``` 
Upload your Markdown as `static/docs.md` and you’re done. 
-->
