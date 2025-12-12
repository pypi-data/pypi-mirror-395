# syntaxmatrix/agents.py
from __future__ import annotations
import os, re, json, textwrap, requests
import pandas as pd

from typing import Optional, List

from syntaxmatrix import utils
from syntaxmatrix.settings.model_map import GPT_MODELS_LATEST
from .. import profiles as _prof
from ..gpt_models_latest import set_args as _set_args, extract_output_text as _out
from google.genai import types 
import tiktoken
from google.genai.errors import APIError


def token_calculator(total_input_content, llm_profile):

    _client = llm_profile["client"]
    _model = llm_profile["model"]
    _provider = llm_profile["provider"].lower()
    
    if _provider == "google":
        tok = _client.models.count_tokens(
            model=_model,
            contents=total_input_content
        )
        input_prompt_tokens = tok.total_tokens
        return input_prompt_tokens
    
    elif _provider == "anthropic":
        tok = _client.beta.messages.count_tokens(
            model=_model,
            system="calculate the total token for the given prompt",
            messages=[{"role": "user", "content": total_input_content}]
        )
        input_prompt_tokens = tok.input_tokens
        return input_prompt_tokens

    else:
        enc = tiktoken.encoding_for_model(_model)
        input_prompt_tokens = len(enc.encode(total_input_content))
        return input_prompt_tokens    

def mlearning_agent(user_prompt, system_prompt, coding_profile, temperature=0.1, max_tokens=4096):
    """
    Returns:
        (text, usage_dict)

    usage_dict schema (best-effort, depending on provider):
        {
            "provider": str,
            "model": str,
            "input_tokens": int|None,
            "output_tokens": int|None,
            "total_tokens": int|None,
            "error": str|None
        }
    """

    # coding_profile['client'] = _prof.get_client(coding_profile)
    _client = coding_profile["client"]
    _provider = coding_profile["provider"].lower()
    _model = coding_profile["model"]
    
    usage = {
        "provider": _provider,
        "model": _model,
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
    }

    def _clean_text(t):
        if t is None:
            return ""
        if not isinstance(t, str):
            t = str(t)
        return t.strip()

    def _get_usage_val(u, keys):
        """Read usage fields from dicts or objects, resiliently."""
        if u is None:
            return None
        for k in keys:
            try:
                if isinstance(u, dict) and k in u:
                    return u[k]
                if hasattr(u, k):
                    return getattr(u, k)
            except Exception:
                continue
        return None

    # Google
    def google_generate_code():
        nonlocal usage
        """
        Generates content using the Gemini API and calculates token usage
        including Context Overhead for consistency.
        """
        
        try:
            # 1. Client Initialization
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            # 2. API Call
            resp = _client.models.generate_content(
                model=_model,
                contents=[user_prompt],
                config=config,
            )

            # 3. Token Usage Capture and Context Overhead Calculation
            um = resp.usage_metadata
            usage["input_tokens"] = um.prompt_token_count
            usage["output_tokens"] = um.thoughts_token_count
            usage["total_tokens"] = um.total_token_count

            # 4. Response Extraction (same robust logic as before)
            text = getattr(resp, "text", None)
            if isinstance(text, str) and text.strip():
                return text.strip()

            chunks = []
            candidates = getattr(resp, "candidates", None) or []
            for cand in candidates:
                content = getattr(cand, "content", None)
                if content:
                    parts = getattr(content, "parts", None) or []
                    for part in parts:
                        t = getattr(part, "text", None)
                        if t:
                            chunks.append(str(t))
                            
            text = "\n".join(chunks).strip()
            if text:
                return text

            # 5. Handle blocked response
            fb = getattr(resp, "prompt_feedback", None)
            block_reason = getattr(fb, "block_reason", None) if fb else None
            if block_reason and block_reason != types.BlockedReason.REASON_UNSPECIFIED:
                raise RuntimeError(f"{_model} blocked the response. Reason: {block_reason.name}")
            raise RuntimeError(f"{_model} failed to return content due to insufficient data.")

        except APIError as e:
            error_msg = f"Gemini API Error: {e}"
        
        except Exception as e:
            error_msg = f"An unexpected error occurred during API call or processing: {e}"

        # --- Return the error message wrapped in the required output code structure ---
        msg = f"I smxAI have instructed {error_msg}\n"
        return (
            f"# {msg}\n"
            "from syntaxmatrix.display import show\n"
            f"show({msg!r})\n"
        )

    # OpenAI Responses API
    def gpt_models_latest_generate_code():
        nonlocal usage

        def reasoning_and_verbosity():
            reasoning_effort, verbosity = "medium", "medium" 
            if _model == "gpt-5-nano":
                reasoning_effort, verbosity = "low", "low"
            elif _model in ["gpt-5-mini", "gpt-5-codex-mini"]:
                reasoning_effort, verbosity = "medium", "medium"
            elif _model in ["gpt-5", "gpt-5-codex", "gpt-5-pro"]:
                reasoning_effort, verbosity = "high", "high"
            return (reasoning_effort, verbosity)
        try:
            args = _set_args(
                model=_model,
                instructions=system_prompt,
                input=user_prompt,
                previous_id=None,
                store=False,
                reasoning_effort=reasoning_and_verbosity()[0],
                verbosity=reasoning_and_verbosity()[1],
            )
            resp = _client.responses.create(**args)
            
            um = resp.usage
            usage["input_tokens"] = um.input_tokens
            usage["output_tokens"] = um.output_tokens
            usage["total_tokens"] = um.total_tokens

            code = _out(resp).strip()
            if code: 
                return code

            # Try to surface any block reason (safety / policy / etc.)
            block_reason = None
            output = resp.get("output")
            for item in output:
                fr = getattr(item, "finish_reason", None)
                if fr and fr != "stop":
                    block_reason = fr
                    break
            if block_reason:
                raise RuntimeError(f"{_model} stopped with reason: {block_reason}")
            raise RuntimeError(f"{_model} returned an empty response in this section due to insufficient data.")    

        except APIError as e:
            # IMPORTANT: return VALID PYTHON so the dashboard can show the error
            msg = f"I smxAI have instructed {e}"
            return (
                f"# {msg}\n"
                "from syntaxmatrix.display import show\n"
                f"show({msg!r})\n"
            )
        
        except Exception as e:
            # IMPORTANT: return VALID PYTHON so the dashboard can show the error
            msg = f"I smxAI have instructed {e}"
            return (
                f"# {msg}\n"
                "from syntaxmatrix.display import show\n"
                f"show({msg!r})\n"
            )
        
    # Anthropic
    def anthropic_generate_code():  
        nonlocal usage      
        try:        
            resp = _client.messages.create(
                model=_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            um = resp.usage
            usage["input_tokens"] = um.input_tokens
            usage["output_tokens"] = um.output_tokens
            usage["total_tokens"] = um.input_tokens + um.output_tokens
                
            # Extract plain text from Claude-style content blocks
            text_blocks = []
            content = getattr(resp, "content", None) or []
            for block in content:
                t = getattr(block, "text", None)
                if not t and isinstance(block, dict):
                    t = (block.get("text") or "").strip()
                if t:
                    text_blocks.append(str(t))

            text = "\n".join(text_blocks).strip()
            if text:
                return text

            stop_reason = getattr(resp, "stop_reason", None)
            if stop_reason and stop_reason != "end_turn":
                raise RuntimeError(f"{_model} stopped with reason: {stop_reason}")
            raise RuntimeError(f"{_model} returned an empty response in this section due to insufficient data.")
        
        except Exception as e:
            msg = f"I smxAI have instructed {e}\n"
            return (
                f"# {msg}\n"
                "from syntaxmatrix.display import show\n"
                f"show({msg!r})\n"
            )

    # OpenAI Chat Completions
    def openai_sdk_generate_code():
        nonlocal usage
        try:
            resp = _client.chat.completions.create(
                model=_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )



            um = resp.usage
            usage["input_tokens"] = um.prompt_tokens
            usage["output_tokens"] = um.completion_tokens
            usage["total_tokens"] = um.total_tokens

            text = resp.choices[0].message.content
            if text:
                return text

            # Try to surface any block reason (safety / policy / etc.)
            block_reason = None
            choices = getattr(resp, "choices", None) or []
            if choices:
                first = choices[0]
                fr = getattr(first, "finish_reason", None)
                if fr and fr != "stop":
                    block_reason = fr

            if block_reason:
                raise RuntimeError(f"{_model} stopped with reason: {block_reason}")
             # Fallback: nothing useful came back
            raise RuntimeError(f"{_model} returned nothing in this section due to insufficient data.")
        
        except Exception as e:
            # IMPORTANT: return VALID PYTHON so the dashboard can show the error
            msg = f"I smxAI have instructed {e}"
            return (
                f"# {msg}\n"
                "from syntaxmatrix.display import show\n"
                f"show({msg!r})\n"
            )

    # print("TTOOKKEENN: ", token_calculator(system_prompt + user_prompt, coding_profile))   

    if _provider == "google":
        code = google_generate_code()
    elif _provider == "openai" and _model in GPT_MODELS_LATEST:
        code = gpt_models_latest_generate_code()
    elif _provider == "anthropic":
        code = anthropic_generate_code()
    else:
        code = openai_sdk_generate_code()

    return code, usage
    

def refine_question_agent(raw_question: str, dataset_context: str | None = None) -> str:
    
    def response_agent(user_prompt, system_prompt, llm_profile, temp=0.0, max_tokens=128):
        _profile = llm_profile
        
        _client = _profile["client"]
        _provider = _profile["provider"].lower()
        _model = _profile["model"]
        
        # Google GenAI
        if _provider == "google":
            resp = _client.models.generate_content(
                model=_model,
                contents=system_prompt + "\n\n" + user_prompt,
            )
            text = resp.text
            return text.strip()       

        # OpenAI 
        elif _provider == "openai" and _model in GPT_MODELS_LATEST: 
            
            def reasoning_and_verbosity():
                reasoning_effort, verbosity = "medium", "medium" 
                if _model == "gpt-5-nano":
                    if max_tokens <= 256:
                        reasoning_effort = "minimal"
                    else: reasoning_effort = "low"
                elif _model in ["gpt-5-mini", "gpt-5-codex-mini"]:
                    verbosity = "medium"
                elif _model in ["gpt-5", "gpt-5-codex", "gpt-5-pro"]:
                    reasoning_effort = "high" 
                    verbosity = "high"
                return (reasoning_effort, verbosity)
        
            args = _set_args(
                model=_model,
                instructions=system_prompt,
                input=user_prompt,
                previous_id=None,
                store=False,
                reasoning_effort=reasoning_and_verbosity()[0],
                verbosity=reasoning_and_verbosity()[1],
            )
            resp = _client.responses.create(**args)
            txt = _out(resp)
            return txt
        
        # Anthropic
        elif _provider == "anthropic":
            try:
                resp = _client.messages.create(
                    model=_model,
                    system=system_prompt,                 
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=0.2,
                    max_tokens= max_tokens,
                )

                # Extract plain text from Claude's content blocks
                text = ""
                content = getattr(resp, "content", None)
                if content and isinstance(content, list):
                    parts = []
                    for block in content:
                        # blocks typically like {"type": "text", "text": "..."}
                        t = getattr(block, "text", None)
                        if not t and isinstance(block, dict):
                            t = block.get("text")
                        if t:
                            parts.append(t)
                    text = " ".join(parts)
                    return text
            except Exception:
                pass

        # OpenAI SDK Compartible (Chat Completions)
        else:
            resp = _client.chat.completions.create(
                model=_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temp,
                max_tokens=max_tokens,
            )
            text = resp.choices[0].message.content
            return text

        return "Configure LLM Profiles or contact your administrator."

    system_prompt = ("""
        - You are a Machine Learning (ML) and Data Science (DS) expert.
        - You rewrite user questions into clear ML job specifications to help AI assistant generate Python code that provides solution to the user question when it is run. Most user questions are vague. So, your goal is to ensure that your output guards the assistant agains making potential errors that you anticipated could arise due to the nature of the question. 
        - If a dataset summary is provided, use it to respect column and help you rewrite the question properly.
        - DO NOT write andy prelude or preamble"
    """)

    user_prompt = f"User question:\n{raw_question}\n\n"
    if dataset_context:
        user_prompt += f"Dataset summary:\n{dataset_context}\n"

    _refiner_profile =  _prof.get_profile("classification") or _prof.get_profile("admin")
    if not _refiner_profile:
        return "ERROR"

    _refiner_profile['client'] = _prof.get_client(_refiner_profile)

    refined_question = response_agent(user_prompt, system_prompt, _refiner_profile, temp=0.0, max_tokens=128)
    return refined_question
  

def classify_ml_job_agent(refined_question, dataset_profile):   
    
    def ml_response(user_prompt, system_prompt, profile):
        _profile = profile  # _prof.get_profile["admin"]
        
        _client = _profile["client"]
        _provider = _profile["provider"].lower()
        _model = _profile["model"]

        prompt = user_prompt + "\n\n" + system_prompt
        
        # Google GenAI
        if _provider == "google":  
            from google.genai.errors import APIError

            config=dict(
                        temperature=0.0,
                        response_mime_type="application/json",
                        # Enforcing a JSON array of strings structure for reliable parsing
                        response_schema={
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    )
            try:
                response = _client.models.generate_content(
                    model=_model,
                    contents=prompt,
                    config=config,
                )         
                json_string = response.text.strip()
                ml_jobs = json.loads(json_string)
                
                if not isinstance(ml_jobs, list) or not all(isinstance(job, str) for job in ml_jobs):
                    return []                  
                return ml_jobs

            except APIError as e:
                return [f"An API error occurred: {e}"]
            except json.JSONDecodeError as e:
                if 'response' in locals():
                    return [f"Raw response text: {response.text}"]
            except Exception as e:
                return [f"An unexpected error occurred: {e}"]
    
        elif _provider == "openai" and _model in GPT_MODELS_LATEST:
            
            def reasoning_and_verbosity():
                reasoning_effort, verbosity = "medium", "medium" 
                if _model == "gpt-5-nano":
                    reasoning_effort = "low"
                elif _model in ["gpt-5-mini", "gpt-5-codex-mini"]:
                    verbosity = "medium"
                elif _model in ["gpt-5", "gpt-5-codex", "gpt-5-pro"]:
                    reasoning_effort = "high" 
                    verbosity = "high"
                return (reasoning_effort, verbosity)
        
            args = _set_args(
                model=_model,
                instructions=system_prompt,
                input=user_prompt,
                previous_id=None,
                store=False,
                reasoning_effort=reasoning_and_verbosity()[0],
                verbosity=reasoning_and_verbosity()[1],
            )
            resp = _client.responses.create(**args)
            txt = _out(resp)
            return txt

        elif _provider == "anthropic":
            try:
                resp = _client.messages.create(
                    model=_model,
                    system=system_prompt,                 
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=0.0,
                    max_tokens= 128,
                )

                # Extract plain text from Claude's content blocks
                text = ""
                content = getattr(resp, "content", None)
                if content and isinstance(content, list):
                    parts = []
                    for block in content:
                        # blocks typically like {"type": "text", "text": "..."}
                        t = getattr(block, "text", None)
                        if not t and isinstance(block, dict):
                            t = block.get("text")
                        if t:
                            parts.append(t)
                    text = " ".join(parts)
                    return text
            except Exception:
                pass

        else:
            resp = _client.chat.completions.create(
                model=_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=128,
            )
            text = resp.choices[0].message.content
            return text

        return "Configure LLM Profiles or contact your administrator."

    system_prompt = ("""
        You are a strict machine learning task classifier for an ML workbench.
        Your goal is to correctly label the user's task specifications with the most relevant tags from a fixed list.
        You Must always have 'data_preprocessing' as the 1st tag. Then add up to 4 to make 5 max. Your list, therefore, should have 1-5 tags. If you think a task is too complext for the given context, even if relevant, exclude it.
        If no relevant tag, default to "data_preprocessing" and return that alone.
        You should return only your list of tags, no prelude or preamble.
    """)

    # --- 1. Define the Master List of ML Tasks (Generalized) ---
    ml_task_list = [
        # Supervised Learning
        "classification", "regression", "ranking", "object_detection", "image_segmentation",
        
        # Unsupervised Learning
        "clustering", "dimensionality_reduction", "anomaly_detection", "association_rule_mining",
        
        # Sequential/Time Data
        "time_series_forecasting", "sequence_labeling", "survival_analysis",
        
        # Specialized Domains
        "natural_language_processing", "computer_vision", "reinforcement_learning", 
        "generative_modeling", "causal_inference", "risk_modeling", "graph_analysis",
        
        # Foundational/Pipeline Steps
        "feature_engineering", "statistical_inference", "data_preprocessing", 
        "model_validation", "hyperparameter_tuning"
    ]
    
    # --- 2. Construct the Generalized Prompt for the LLM ---
    task_description = refined_question

    user_prompt = f"""
    Analyze the following task description:
    ---
    {task_description}
    ---
    
    If the Dataset Profile is provided, use its info, together with the task description, to make your job types
    Identify and select ALL job types from the provided, extensive list that are directly 
    relevant to achieving the goals outlined in the task description (either as the 
    core goal, prerequisites, or essential steps).
    
    ML Jobs List: {', '.join(ml_task_list)}

    Respond ONLY with a valid JSON array of strings containing the selected ML job names.
    Example Response: ["natural_language_processing", "classification", "feature_engineering"]
    """

    if dataset_profile:
        user_prompt += f"\nDataset profile:\n{dataset_profile}\n"
        
    llm_profile =  _prof.get_profile("classification") or _prof.get_profile("admin")
    if not llm_profile:
        return "ERROR"

    llm_profile['client'] = _prof.get_client(llm_profile)

    # Extract raw content
    tasks = ml_response(user_prompt, system_prompt, llm_profile)
    return tasks


def text_formatter_agent(text):
    """
    Parses an ML job description using the Gemini API with Structured JSON Output.
    """
    
    def generate_formatted_report(data):
        """
        Generates a formatted string of the structured data in a clean, 
        document-like format mimicking the requested list structure.
        
        Returns:
            str: The complete formatted report as a string.
        """
        if not data:
            return "No data to display."

        output_lines = []

        # --- Helper Functions ---
        def clean_md(text):
            """Removes markdown bold syntax."""
            return text.replace("**", "")

        def format_smart_list_item(prefix, item_text, width=80):
            """
            Content-agnostic list formatter.
            Detects 'Header: Description' patterns and formats them inline.
            Returns the formatted string.
            """
            cleaned = clean_md(item_text)
            
            # Check for "Header: Description" pattern
            # We look for a colon appearing early in the string (e.g., within first 60 chars)
            colon_match = re.match(r"^([^:]{1,60}):\s*(.*)", cleaned, re.DOTALL)
            
            if colon_match:
                header = colon_match.group(1).strip()
                description = colon_match.group(2).strip()
                
                # Format: PREFIX HEADER: Description
                full_line = f"{prefix} {header.upper()}: {description}\n"
            else:
                # Format: PREFIX Content
                full_line = f"{prefix} {cleaned}\n"

            # Calculate hanging indent (aligning with the start of the text after the prefix)
            # Length of prefix + 1 space
            indent_width = len(prefix) + 1
            hanging_indent = " " * indent_width
            
            return textwrap.fill(
                full_line, 
                width=width, 
                subsequent_indent=hanging_indent
            )

        # --- Report Construction ---

        # 1. Title
        title = clean_md(data.get("project_title", "Project Report"))
        output_lines.append("\n" + "=" * 80)
        output_lines.append(f"{title.center(80)}")
        output_lines.append("=" * 80 + "\n")

        # 2. Project Goal
        output_lines.append("PROJECT GOAL\n")
        output_lines.append("-" * 12)
        goal = clean_md(data.get("project_goal", ""))
        output_lines.append(textwrap.fill(goal, width=80))
        output_lines.append("") # Adds a blank line

        # 3. Key Objectives
        if data.get("key_objectives"):
            output_lines.append("KEY OBJECTIVES & STRATEGIC INSIGHTS")
            output_lines.append("-" * 35)
            for item in data["key_objectives"]:
                output_lines.append(format_smart_list_item("•", item))
            output_lines.append("")

        # 4. ML Tasks (Numbered List)
        if data.get("ml_tasks"):
            output_lines.append("ML EXECUTION TASKS")
            output_lines.append("-" * 18)
            for i, task in enumerate(data["ml_tasks"], 1):
                # Using i. as prefix
                output_lines.append(format_smart_list_item(f"{i}.", task))
            output_lines.append("")

        # 5. Deliverables
        if data.get("expected_deliverables"):
            output_lines.append("EXPECTED DELIVERABLES")
            output_lines.append("-" * 21)
            for item in data["expected_deliverables"]:
                output_lines.append(format_smart_list_item("•", item))
        output_lines.append("")

        # Join all lines with newlines
        return "\n".join(output_lines)

    formatter_profile = _prof.get_profile("classification") or _prof.get_profile("classification")
    _api_key = formatter_profile["api_key"]
    _provider = formatter_profile["provider"]
    _model = formatter_profile["model"]
    
    # 1. Define the Schema for strict JSON enforcement
    schema = {
        "type": "OBJECT",
        "properties": {
            "project_title": {"type": "STRING"},
            "project_goal": {"type": "STRING"},
            "key_objectives": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
            "data_inputs": {
                "type": "OBJECT",
                "properties": {
                    "description_items": {
                        "type": "ARRAY", 
                        "items": {"type": "STRING"}
                    },
                    "extracted_features": {
                        "type": "ARRAY", 
                        "items": {"type": "STRING"},
                        "description": "List of specific column names or features mentioned (e.g. Age, BMI)"
                    }
                }
            },
            "ml_tasks": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
            "expected_deliverables": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            }
        },
        "required": ["project_title", "project_goal", "key_objectives", "data_inputs", "ml_tasks"]
    }

    # 2. Construct the API Request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{_model}:generateContent?key={_api_key}"
    
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Extract the structured data from the following ML Job Description:\n\n{text}"
            }]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": schema
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_json = response.json()
        
        # 4. Extract and Parse Content
        raw_text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
        parsed_data = json.loads(raw_text_response)

        report = generate_formatted_report(parsed_data)
        return parsed_data

    except requests.exceptions.RequestException as e:
        if 'response' in locals() and response is not None:
             return (f"API Request Failed: {e}\n\nResponse info: {response.text}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"Parsing Failed: {e}"


