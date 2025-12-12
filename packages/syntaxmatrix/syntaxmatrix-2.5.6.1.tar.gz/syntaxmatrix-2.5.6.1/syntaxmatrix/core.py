from __future__ import annotations
import ast
import textwrap
import os, webbrowser, uuid, secrets, re

from flask import Flask, Response, session, request, has_request_context
from syntaxmatrix.agentic.agents import mlearning_agent
from syntaxmatrix.history_store import SQLHistoryStore as Store, PersistentHistoryStore as _Store
from collections import OrderedDict
from syntaxmatrix.llm_store import save_embed_model, load_embed_model, delete_embed_key
from . import db, routes
from .themes import DEFAULT_THEMES
from .ui_modes import UI_MODES
from .plottings import render_plotly, pyplot, describe_plotly
from .file_processor import process_admin_pdf_files
from google.genai import types
from .vector_db import query_embeddings
from .vectorizer import embed_text
from syntaxmatrix.settings.prompts import SMXAI_CHAT_ID, SMXAI_CHAT_INSTRUCTIONS, SMXAI_WEBSITE_DESCRIPTION
from typing import List, Generator
from .auth import init_auth_db
from . import profiles as _prof
from syntaxmatrix.smiv import SMIV
from .project_root import detect_project_root
from syntaxmatrix.gpt_models_latest import extract_output_text as _out, set_args 
from dotenv import load_dotenv
from html import unescape
from .plottings import render_plotly, pyplot, describe_plotly, describe_matplotlib
from threading import RLock
from syntaxmatrix.settings.model_map import GPT_MODELS_LATEST


# ──────── framework‐local storage paths ────────
# this ensures the key & data always live under the package dir,
# regardless of where the developer `cd` into before launching.
_CLIENT_DIR = detect_project_root()
_HISTORY_DIR   = os.path.join(_CLIENT_DIR, "smx_history")
os.makedirs(_HISTORY_DIR, exist_ok=True)

_SECRET_PATH = os.path.join(_CLIENT_DIR, ".smx_secret_key")

_CLIENT_DOTENV_PATH = os.path.join(str(_CLIENT_DIR.parent), ".env")
if os.path.isfile(_CLIENT_DOTENV_PATH):
    load_dotenv(_CLIENT_DOTENV_PATH, override=True)

_ICONS_PATH = os.path.join(_CLIENT_DIR, "static", "icons")
os.makedirs(_ICONS_PATH, exist_ok=True)

EDA_OUTPUT = {}  # global buffer for EDA output by session

class SyntaxMUI:
    def __init__(self, 
           host="127.0.0.1", 
            port="5080", 
            user_icon="👩🏿‍🦲",
            bot_icon="<img src='/static/icons/favicon.png' width=20' alt='bot'/>",
            favicon="",  # /static/icons/favicon.png",      
            site_logo="<img src='/static/icons/logo.png' width='30' alt='logo'/>",           
            site_title="SyntaxMatrix", 
            project_name="smxAI", 
            theme_name="light",
            ui_mode = "default"
        ):
        self.app = Flask(__name__)         
        self.host = host
        self.port = port

        self.get_app_secrete()
        self.user_icon = user_icon
        self.bot_icon = bot_icon
        self.site_logo = site_logo
        self.favicon = favicon
        self.site_title = site_title
        self.project_name = project_name
        self.ui_mode = ui_mode
        self.theme_toggle_enabled = False
        self.user_files_enabled = False
        self.registration_enabled = False
        self.smxai_identity = SMXAI_CHAT_ID
        self.smxai_instructions = SMXAI_CHAT_INSTRUCTIONS    
        self.website_description = SMXAI_WEBSITE_DESCRIPTION
        self._eda_output = {}      # {chat_id: html}
        self._eda_lock = RLock()
        
        db.init_db()
        self.page = ""
        self.pages = db.get_pages()
        init_auth_db() 

        self.widgets = OrderedDict()
        self.theme = DEFAULT_THEMES.get(theme_name, DEFAULT_THEMES["light"])     
        self.system_output_buffer = ""  # Ephemeral buffer initialized  
        self.app_token = str(uuid.uuid4())  # NEW: Unique token for each app launch.
        self.admin_pdf_chunks = {}   # In-memory store for admin PDF chunks
        self.user_file_chunks = {}  # In-memory store of user‑uploaded chunks, scoped per chat session
        
        self._last_llm_usage = None 
        routes.setup_routes(self)

        self._admin_profile = {}
        self._chat_profile = {}
        self._coding_profile = {}
        self._classification_profile = {}
        self._summarization_profile = {}
            
        self._gpt_models_latest_prev_resp_ids = {}
        self.is_streaming = False
        self.stream_args = {}

        self._recent_visual_summaries = []

        self.placeholder = ""

    @staticmethod
    def init_app(app):
        import secrets
        if not app.secret_key:
            app.secret_key = secrets.token_urlsafe(32)

    def get_app_secrete(self): 
        if os.path.exists(_SECRET_PATH):
            self.app.secret_key = open(_SECRET_PATH, "r", encoding="utf-8").read().strip()
        else:
            new_key = secrets.token_urlsafe(32)
            with open(_SECRET_PATH, "w", encoding="utf-8") as f:
                f.write(new_key)
            try:
                os.chmod(_SECRET_PATH, 0o600)
            except Exception:
                pass
            self.app.secret_key = new_key
            

    def _get_visual_context(self):
        """Return the concatenated summaries for prompt injection."""
        if not self._recent_visual_summaries:
            return ""
        joined = "\n• " + "\n• ".join(self._recent_visual_summaries)
        return f"\n\nRecent visualizations:{joined}"

    # add to class
    def _add_visual_summary(self, summary: str) -> None:
        if not summary:
            return
        if not hasattr(self, "_recent_visual_summaries"):
            self._recent_visual_summaries = []
        # keep last 6
        self._recent_visual_summaries = (self._recent_visual_summaries + [summary])[-6:]

    def set_plottings(self, fig_or_html, note=None):
        # prefer current chat id; fall back to per-browser sid; finally "default"
        sid = self.get_session_id() or self._sid() or "default"

        # Clear for this session if empty/falsy
        if not fig_or_html or (isinstance(fig_or_html, str) and fig_or_html.strip() == ""):
            with self._eda_lock:
                self._eda_output.pop(sid, None)
            return

        html = None

        # ---- Plotly Figure support ----
        try:
            import plotly.graph_objs as go
            if isinstance(fig_or_html, go.Figure):
                html = fig_or_html.to_html(full_html=False)
        except ImportError:
            pass

        # ---- Matplotlib Figure support ----
        if html is None and hasattr(fig_or_html, "savefig"):
            html = pyplot(fig_or_html)

        # ---- Bytes (PNG etc.) support ----
        if html is None and isinstance(fig_or_html, bytes):
            import base64
            img_b64 = base64.b64encode(fig_or_html).decode()
            html = f"<img src='data:image/png;base64,{img_b64}'/>"

        # ---- HTML string support ----
        if html is None and isinstance(fig_or_html, str):
            html = fig_or_html

        if html is None:
            raise TypeError("Unsupported object type for plotting.")

        if note:
            html += f"<div style='margin-top:10px; text-align:center; color:#888;'><strong>{note}</strong></div>"

        wrapper = f'''
        <div style="
            position:relative; max-width:650px; margin:30px auto 20px auto;
            padding:20px 28px 10px 28px; background:#fffefc;
            border:2px solid #2da1da38; border-radius:16px;
            box-shadow:0 3px 18px rgba(90,130,230,0.06); min-height:40px;">
            <button id="eda-close-btn" onclick="closeEdaPanel()" style="
                position: absolute; top: 20px; right: 12px;
                font-size: 1.25em; background: transparent;
                border: none; color: #888; cursor: pointer;
                z-index: 2; transition: color 0.2s;">&times;</button>
            {html}
        </div>
        '''

        with self._eda_lock:
            self._eda_output[sid] = wrapper

        html = None

        # ---- Plotly Figure support ----
        try:
            import plotly.graph_objs as go
            if isinstance(fig_or_html, go.Figure):
                html = fig_or_html.to_html(full_html=False)
        except ImportError:
            pass

        # ---- Matplotlib Figure support ----
        if html is None and hasattr(fig_or_html, "savefig"):
            html = pyplot(fig_or_html)

        # ---- Bytes (PNG etc.) support ----
        if html is None and isinstance(fig_or_html, bytes):
            import base64
            img_b64 = base64.b64encode(fig_or_html).decode()
            html = f"<img src='data:image/png;base64,{img_b64}'/>"

        # ---- HTML string support ----
        if html is None and isinstance(fig_or_html, str):
            html = fig_or_html

        if html is None:
            raise TypeError("Unsupported object type for plotting.")

        if note:
            html += f"<div style='margin-top:10px; text-align:center; color:#888;'><strong>{note}</strong></div>"

        wrapper = f'''
        <div style="
            position:relative; max-width:650px; margin:30px auto 20px auto;
            padding:20px 28px 10px 28px; background:#fffefc;
            border:2px solid #2da1da38; border-radius:16px;
            box-shadow:0 3px 18px rgba(90,130,230,0.06); min-height:40px;">
            <button id="eda-close-btn" onclick="closeEdaPanel()" style="
                position: absolute; top: 20px; right: 12px;
                font-size: 1.25em; background: transparent;
                border: none; color: #888; cursor: pointer;
                z-index: 2; transition: color 0.2s;">&times;</button>
            {html}
        </div>
        '''
        EDA_OUTPUT[sid] = wrapper


    def get_plottings(self):
        sid = self.get_session_id() or self._sid() or "default"
        with self._eda_lock:
            return self._eda_output.get(sid, "")
    

    def load_sys_chunks(self, directory: str = "uploads/sys"):
        """
        Process all PDFs in `directory`, store chunks in DB and cache in-memory.
        Returns mapping { file_name: [chunk, ...] }.
        """
        mapping = process_admin_pdf_files(directory)
        self.admin_pdf_chunks = mapping
        return mapping


    def smpv_search(self, q_vec: List[float], top_k: int = 5):
        """
        Embed the input text and return the top_k matching PDF chunks.
        Each result is a dict with keys:
        - 'id': the embedding record UUID
        - 'score': cosine similarity score (0–1)
        - 'metadata': dict, e.g. {'file_name': ..., 'chunk_index': ...}
        """
        # 2) Fetch nearest neighbors from our sqlite vector store
        results = query_embeddings(q_vec, top_k=top_k)
        return results


    def set_ui_mode(self, mode):
        if mode not in self.get_ui_modes():  # ["default", "card", "bubble", "smx"]:
            raise ValueError("UI mode must be one of: 'default', 'card', 'bubble', 'smx'.")
        self.ui_mode = mode

    @staticmethod
    def get_ui_modes():
        return list(UI_MODES.keys())
        # return "default", "card", "bubble", "smx"
    
    @staticmethod
    def get_themes():
        return list(DEFAULT_THEMES.keys())


    def set_theme(self, theme_name, theme=None):
        if theme_name in DEFAULT_THEMES:
            self.theme = DEFAULT_THEMES[theme_name]
        elif isinstance(theme, dict):
            DEFAULT_THEMES[theme_name] = theme
            self.theme = DEFAULT_THEMES[theme_name]
        else:
            self.theme = DEFAULT_THEMES["light"]
            self.error("Theme must be 'light', 'dark', or a custom dict.")

    
    def enable_theme_toggle(self):
        self.theme_toggle_enabled = True 
    
    def enable_user_files(self):
        self.user_files_enabled = True

    def enable_registration(self):
        self.registration_enabled = True
    
    @staticmethod
    def columns(components):
        col_html = "<div style='display:flex; gap:10px;'>"
        for comp in components:
            col_html += f"<div style='flex:1;'>{comp}</div>"
        col_html += "</div>"
        return col_html

    def set_site_title(self, title):
        self.site_title = title
    
    def set_project_name(self, project_name):
        self.project_name = project_name

    def set_favicon(self, icon):
        self.favicon = icon

    def set_site_logo(self, logo):
        self.site_logo = logo

    def set_user_icon(self, icon):
        self.user_icon = icon

    def set_bot_icon(self, icon):
        self.bot_icon = icon

    def text_input(self, key, id, label, placeholder=""):
        if not placeholder:
            placeholder = f"Ask {self.project_name} anything"
        if key not in self.widgets:
            self.widgets[key] = {
                "type": "text_input", "key": key, "id": id,
                "label": label, "placeholder": placeholder
            }

    def clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True
    

    def button(self, key, id, label, callback, stream=False):
        if stream == True:
            self.is_streaming = True
        self.widgets[key] = {
            "type": "button", "key": key, "id": id, "label": label, "callback": callback, "stream":stream
        }

    def file_uploader(self, key, id, label, accept_multiple_files):
        if key not in self.widgets:
            self.widgets[key] = {
                "type": "file_upload",
                "key": key, "id":id, "label": label,
                "accept_multiple": accept_multiple_files,
        }


    def get_file_upload_value(self, key):
        return session.get(key, None)
    

    def dropdown(self, key, options, label=None, callback=None):
        self.widgets[key] = {
            "type": "dropdown",
            "key": key,
            "label": label if label else key,
            "options": options,
            "callback": callback,
            "value": options[0] if options else None
        }


    def get_widget_value(self, key):
        return self.widgets[key]["value"] if key in self.widgets else None


    # ──────────────────────────────────────────────────────────────
    # Session-safe chat-history helpers
    # ──────────────────────────────────────────────────────────────
    @staticmethod
    def _sid() -> str:
        sid = session.get("_smx_sid")
        if not sid:
            # use the new _sid helper on the store instead of the old ensure_session_id
            sid = _Store._sid(request.cookies.get("_smx_sid"))
        session["_smx_sid"] = sid
        session.modified = True
        return sid
    
    def get_chat_history(self) -> list[tuple[str, str]]:
        # Load the history for the _current_ chat session
        sid = self._sid()
        cid = self.get_session_id()
        if session.get("user_id"):
            # Logged-in: use SQLHistoryStore (Store). Locking handled inside history_store.py
            return Store.load(str(session["user_id"]), cid)
        # Anonymous: use PersistentHistoryStore (_Store) JSON files
        return _Store.load(sid, cid)


    def set_chat_history(self, history: list[tuple[str, str]], *, max_items: int | None = None) -> list[tuple[str, str]]:
        sid = self._sid()
        cid = self.get_session_id()
        if session.get("user_id"):
            # Logged-in: chats.db via Store (SQLHistoryStore)
            Store.save(str(session["user_id"]), cid, history)
        else:
            # Anonymous: file-backed via _Store (PersistentHistoryStore)
            _Store.save(sid, cid, history)


    def clear_chat_history(self):
        if has_request_context():
            sid = self._sid()
            cid = self.get_session_id()

            # delete the chat from the correct backend (DB for logged-in, file for anonymous)
            if session.get("user_id"):
                Store.delete(session["user_id"], cid)
            else:
                _Store.delete(sid, cid)

            # rotate to a fresh empty chat (session remains metadata-only)
            new_cid = str(uuid.uuid4())
            session["current_session"] = {"id": new_cid, "title": "Current"}
            session["active_chat_id"] = new_cid
            session.modified = True
    
    def bot_message(self, content, max_length=20):
        history = self.get_chat_history()
        history.append(("Bot", content))
        self.set_chat_history(history)


    def plt_plot(self, fig):
        summary = describe_matplotlib(fig)
        self._add_visual_summary(summary)          
        html = pyplot(fig)
        self.bot_message(html)

    def plotly_plot(self, fig):
        try:
            summary = describe_plotly(fig)
            self._add_visual_summary(summary)      
            html = render_plotly(fig)
            self.bot_message(html)
        except Exception as e:
            self.error(f"Plotly rendering failed: {e}")


    def write(self, content):
        self.bot_message(content)

    def stream_write(self, chunk: str, end=False):
        """Push a token to the SSE queue and, when end=True,
        persist the whole thing to chat_history."""
        from .routes import _stream_q
        _stream_q.put(chunk)              # live update
        if end:                           # final flush → history
            self.bot_message(chunk)       # persists the final message


    def error(self, content):
        self.bot_message(f'<div style="color:red; font-weight:bold;">{content}</div>')


    def warning(self, content):
        self.bot_message(f'<div style="color:orange; font-weight:bold;">{content}</div>')


    def success(self, content):
        self.bot_message(f'<div style="color:green; font-weight:bold;">{content}</div>')


    def info(self, content):
        self.bot_message(f'<div style="color:blue;">{content}</div>')

    
    def get_session_id(self):
        """Return the chat id that is currently *active* in the UI."""
        # Prefer a sticky id set by /load_session or when a new chat is started.
        sticky = session.get("active_chat_id")
        if sticky:
            return sticky
        return session.get("current_session", {}).get("id")

    def add_user_chunks(self, session_id, chunks):
        """Append these text‐chunks under that session’s key."""
        self.user_file_chunks.setdefault(session_id, []).extend(chunks)


    def get_user_chunks(self, session_id):
        """Get any chunks that this session has uploaded."""
        return self.user_file_chunks.get(session_id, [])


    def clear_user_chunks(self, session_id):
        """Remove all stored chunks for a session (on chat‑clear or delete)."""
        self.user_file_chunks.pop(session_id, None)

    # ──────────────────────────────────────────────────────────────
    #  *********** LLM CLIENT HELPERS  **********************
    # ──────────────────────────────────────────────────────────────
    def set_smxai_identity(self, profile):
        self.set_smxai_identity = profile
    

    def set_smxai_instructions(self, instructions):
        self.set_smxai_instructions = instructions


    def set_website_description(self, desc):
        self.website_description = desc


    def embed_query(self, q):
        return embed_text(q)
    
    def smiv_index(self, sid):
            chunks = self.get_user_chunks(sid) or []
            count = len(chunks)

            # Ensure the per-session index stores for user text exist
            if not hasattr(self, "_user_indices"):
                self._user_indices = {}              # gloval dict for user vecs
                self._user_index_counts = {}         # global dict of user vec counts

            # store two maps: _user_indices and _user_index_counts
            if (sid not in self._user_indices or self._user_index_counts.get(sid, -1) != count):
                # (re)build
                try:
                    vecs = [embed_text(txt) for txt in chunks]
                except Exception as e:
                    # show the embedding error in chat and stop building the index
                    self.error(f"Failed to embed user documents: {e}")
                    return None
                index = SMIV(len(vecs[0]) if vecs else 1536)
                for i,(txt,vec) in enumerate(zip(chunks,vecs)):
                    index.add(vector=vec, metadata={"chunk_text": txt, "chunk_index": i, "session_id": sid})
                self._user_indices[sid] = index
                self._user_index_counts[sid] = count
            return self._user_indices[sid]

    def load_embed_model(self):
        client = load_embed_model()
        os.environ["PROVIDER"] = client["provider"]
        os.environ["MAIN_MODEL"] = client["model"]
        os.environ["OPENAI_API_KEY"] = client["api_key"]
        return client
    
    def save_embed_model(self, provider:str, model:str, api_key:str):
        return save_embed_model(provider, model, api_key)
    
    def delete_embed_key(self):
        return delete_embed_key()


    def get_gpt_models_latest(self):
        return GPT_MODELS_LATEST

    def get_text_input_value(self, key, default=""):
        q = session.get(key, default)
        
        intent = self.classify_query_intent(q)         
        intent = intent.strip().lower() if intent else ""
        if intent not in {"none","user_docs","system_docs","hybrid"}:
            self.error("Classify agency error")
            return q, None
        return q, intent

    def enable_stream(self):
        self.is_streaming = True 
    
    def stream(self):
        return self.is_streaming
    
    def get_stream_args(self):
        return self.stream_args


    def classify_query_intent(self, query: str) -> str:
        from syntaxmatrix.gpt_models_latest import extract_output_text as _out, set_args 
   
        if not self._classification_profile:
            classification_profile = _prof.get_profile('classification') or _prof.get_profile('chat') or _prof.get_profile('admin')
            if not classification_profile:
                return {"Error": "Set a profile for Classification"}
            self._classification_profile = classification_profile
            self._classification_profile['client'] = _prof.get_client(classification_profile)

        _client = self._classification_profile['client']
        _provider = self._classification_profile['provider']
        _model = self._classification_profile['model']

        # New instruction format with hybrid option
        _intent_profile = "You are an intent classifier. Respond ONLY with the intent name."
        _instructions = f"""
            Classify the given query into ONE of these intents You must return ONLY the intent name with no comment or any preamble:
            - "none": Casual chat/greetings
            - "user_docs": Requires user-uploaded documents
            - "system_docs": Requires company knowledge/docs
            - "hybrid": Requires BOTH user docs AND company docs
            
            Examples:
            Query: "Hi there!" → none
            Query: "Explain my uploaded contract" → user_docs
            Query: "What's our refund policy?" → system_docs
            Query: "How does my proposal align with company guidelines?" → hybrid
            Query: "What is the weather today?" → none
            Query: "Cross-reference the customer feedback from my uploaded survey results with our product's feature list in the official documentation." → hybrid

            Now classify:
            Query: "{query}"
            Intent: 
        """
        openai_sdk_messages = [
            {"role": "system", "content": _intent_profile},
            {"role": "user", "content": _instructions}
        ]

        def google_classify_query():
            response = _client.models.generate_content(
                model=_model,
                contents=f"{_intent_profile}\n{_instructions}\n\n"
            )
            return response.text.strip().lower()

        def gpt_models_latest_classify_query(reasoning_effort = "medium", verbosity = "low"):
                             
            args = set_args(
                model=_model,
                instructions=_intent_profile,
                input=_instructions,
                reasoning_effort=reasoning_effort,
                verbosity=verbosity,
            )
            try:
                resp = _client.responses.create(**args)
                answer = _out(resp).strip().lower() 
                return answer if answer else ""
            except Exception as e:
                return f"Error!"
        
        def anthropic_classify_query():       
            try:
                response = _client.messages.create(
                    model=_model,
                    max_tokens=1024,
                    system=_intent_profile,
                    messages=[{"role": "user", "content":_instructions}],
                    stream=False,
                )
                return response.content[0].text.strip()    
                   
            except Exception as e:
                return f"Error: {str(e)}"

        def openai_sdk_classify_query():
            try:
                response = _client.chat.completions.create(
                    model=_model,
                    messages=openai_sdk_messages,
                    temperature=0,
                    max_tokens=100
                )
                intent = response.choices[0].message.content.strip().lower()
                return intent if intent else ""
            except Exception as e:
                return f"Error!"

        if _provider == "google":
            intent = google_classify_query()
            return intent
        if _model in self.get_gpt_models_latest():
            intent = gpt_models_latest_classify_query()
            return intent
        if _provider == "anthropic":
            intent = anthropic_classify_query()
            return intent
        else:
            intent = openai_sdk_classify_query()
            return intent
     

    def generate_contextual_title(self, chat_history):
        
        if not self._summarization_profile:
            summarization_profile = _prof.get_profile('summarization') or _prof.get_profile('chat') or _prof.get_profile('admin') 
            if not summarization_profile:
                return {"Error": "Chat profile not set yet."}
            
            self._summarization_profile = summarization_profile
            self._summarization_profile['client'] = _prof.get_client(summarization_profile)

        conversation = "\n".join([f"{role}: {msg}" for role, msg in chat_history])
        _title_profile = "You are a title generator that creates concise and relevant titles for the given conversations."
        _instructions = f"""
            Generate a contextual title (5 short words max) from the given Conversation History 
            The title should be concise - with no preamble, relevant, and capture the essence of this Conversation: \n{conversation}.\n\n
            return only the title.
        """
        
        _client = self._summarization_profile['client']
        _provider = self._summarization_profile['provider']
        _model = self._summarization_profile['model']

        def google_generated_title():
            try:
                response = _client.models.generate_content(
                    model=_model,
                    contents=f"{_title_profile}\n{_instructions}"
                )
                return response.text.strip()
            except Exception as e:
                return f"Summary agent error!"

        def gpt_models_latest_generated_title():
            try:                 
                args = set_args(
                    model=_model,
                    instructions=_title_profile,
                    input=_instructions,
                    # reasoning_effort=reasoning_effort,
                    # verbosity=verbosity,
                )
            
                resp = _client.responses.create(**args)
                return _out(resp).strip()
            except Exception as e:
                return f"Summary agent error!"
        
        def anthropic_generated_title():       
            try:
                response = _client.messages.create(
                    model=_model,
                    max_tokens=50,
                    system=_title_profile,
                    messages=[{"role": "user", "content":_instructions}],
                    stream=False,
                )
                return response.content[0].text.strip()  
            except Exception as e:
                return f"Summary agent error!"
            
        def openai_sdk_generated_title():     
            prompt = [
                { "role": "system", "content": _title_profile }, 
                { "role": "user", "content": _instructions },
            ]
            try:
                response = _client.chat.completions.create(
                    model=_model,
                    messages=prompt,
                    temperature=0.3,
                    max_tokens=50
                ) 
                title = response.choices[0].message.content.strip().lower()
                return title if title else ""
            except Exception as e:
               return f"Summary agent error!"

        if _provider == "google":
            title = google_generated_title()
        elif _model in self.get_gpt_models_latest():
            title = gpt_models_latest_generated_title()
        elif _provider == "anthropic":
            title = anthropic_generated_title()
        else:
            title = openai_sdk_generated_title()
        return title
    

    def stream_process_query(self, query, context, conversations, sources):
        self.stream_args['query'] = query
        self.stream_args['context'] = context
        self.stream_args['conversations'] = conversations
        self.stream_args['sources'] = sources
    

    def process_query_stream(self, query: str, context: str, history: list, stream=True) -> Generator[str, None, None]:
       
        if not self._chat_profile:
            chat_profile = _prof.get_profile("chat") or _prof.get_profile("admin")
            if not chat_profile:
                yield """<p style='color:red;'>Error: Chat profile is not configured. Add a chat profile inside the admin panel or contact your administrator.</p>
                """
                return None
            self._chat_profile = chat_profile
            self._chat_profile['client'] = _prof.get_client(chat_profile)

        _provider = self._chat_profile['provider']
        _client = self._chat_profile['client']
        _model = self._chat_profile['model']

        _contents = f"""
            {self.smxai_instructions}\n\n 
            Question: {query}\n
            Context: {context}\n\n
            History: {history}\n\n
            Use conversation continuity if available.
        """       
        
        try:
            if _provider == "google":     # Google, non openai skd series     
            
                for chunk in _client.models.generate_content_stream(
                    model=_model,
                    contents=_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.smxai_identity,
                        temperature=0.3,
                        max_output_tokens=1024,
                    ),
                ):
            
                    yield chunk.text
        
            elif _provider == "openai" and _model in self.get_gpt_models_latest():  # GPt 5 series
                input_prompt = (
                    f"{self.smxai_instructions}\n\n"
                    f"Generate a response to this query:\n{query}\n"
                    f"based on this given context:\n{context}\n\n"
                    f"(Use conversation continuity if available.)"
                )
                sid = self.get_session_id()
                prev_id = self._gpt_models_latest_prev_resp_ids.get(sid)
                args = set_args(model=_model, instructions=self.smxai_identity, input=input_prompt, previous_id=prev_id, store=True)
                
                with _client.responses.stream(**args) as s:
                    for event in s:
                        if event.type == "response.output_text.delta" and event.delta:
                            yield event.delta
                        elif event.type == "response.error":
                            raise RuntimeError(str(event.error))
                    final = s.get_final_response()
                    if getattr(final, "id", None):
                        self._gpt_models_latest_prev_resp_ids[sid] = final.id
            
            elif _provider == "anthropic":
                with _client.messages.stream(
                    max_tokens=1024,
                    messages=[{"role": "user", "content":f"{self.smxai_identity}\n\n {_contents}"},],
                    model=_model,
                ) as stream:
                    for text in stream.text_stream:
                        yield text  # end="", flush=True
                    
            else:  # Assumes standard openai_sdk
                openai_sdk_prompt = [
                    {"role": "system", "content": self.smxai_identity},
                    {"role": "user", "content": f"{self.smxai_instructions}\n\nGenerate response to this query: {query}\nbased on this context:\n{context}\nand history:\n{history}\n\nUse conversation continuity if available.)"},
                ]
                response = _client.chat.completions.create(
                    model=_model, 
                    messages=openai_sdk_prompt, 
                    stream=True,
                )
                for chunk in response:
                    token = getattr(chunk.choices[0].delta, "content", "")
                    if token:
                        yield token
        except Exception as e:
            yield f"Error during streaming: {type(e).__name__}: {e}"
    
    def process_query(self, query, context, history, stream=False):

        if not self._chat_profile:
            chat_profile = _prof.get_profile("chat") or _prof.get_profile("admin")
            if not chat_profile:
                return """<p style='color:red;'>Error: Chat profile is not configured. Add a chat profile inside the admin panel or contact your administrator.</p>
                """
                return
                 
            self._chat_profile = chat_profile
            self._chat_profile['client'] = _prof.get_client(chat_profile) 
        _provider = self._chat_profile['provider']
        _client = self._chat_profile['client']
        _model = self._chat_profile['model']
        _contents = f"""
                    {self.smxai_instructions}\n\n
                    Question: {query}\n
                    Context: {context}\n\n
                    History: {history}\n\n
                    Use conversation continuity if available.
                """
        
        openai_sdk_prompt = [
                {"role": "system", "content": self.smxai_identity},
                {"role": "user", "content": f"""{self.smxai_instructions}\n\n
                                                Generate response to this query: {query}\n
                                                based on this context:\n{context}\n
                                                and history:\n{history}\n\n
                                                Use conversation continuity if available.)
                                            """
                },
            ]

        def google_process_query():
            try:
                response = _client.models.generate_content(
                    model=_model,
                    contents=_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.smxai_identity,
                        temperature=0.3,
                        max_output_tokens=1024,
                    ),
                )
                answer = response.text

                # answer = strip_html(answer)
                return answer
            except Exception as e:
                return f"Error: {str(e)}"

        def gpt_models_latest_process_query(previous_id: str | None, reasoning_effort = "minimal", verbosity = "low"):
            """
            Returns (answer_text, new_response_id)
            """
            # Prepare the prompt with conversation history and context
            input = (
                f"{self.smxai_instructions}\n\n"
                f"Generate a response to this query:\n{query}\n"
                f"based on this given context:\n{context}\n\n"
                f"(Use conversation continuity if available.)"
            )

            sid = self.get_session_id()
            prev_id = self._gpt_models_latest_prev_resp_ids.get(sid)
            
            args = set_args(
                model=_model,
                instructions=self.smxai_identity,
                input=input,
                previous_id=prev_id,
                store=True,
                reasoning_effort=reasoning_effort,
                verbosity=verbosity
            )
            try:
                # Non-stream path
                resp = _client.responses.create(**args)
                answer = _out(resp)
                if getattr(resp, "id", None):
                    self._gpt_models_latest_prev_resp_ids[sid] = resp.id
                
                # answer = strip_html(answer)
                return answer

            except Exception as e:
                return f"Error: {type(e).__name__}: {e}"
                     
        def anthropic_process_query():      
            try:
                response = _client.messages.create(
                    model=_model,
                    max_tokens=1024,
                    system=self.self.smxai_identity,
                    messages=[{"role": "user", "content":_contents}],
                    stream=False,
                )
                return response.content[0].text.strip()    
                   
            except Exception as e:
                return f"Error: {str(e)}"

        def openai_sdk_process_query():
        
            try:
                response = _client.chat.completions.create(
                    model=_model,
                    messages=openai_sdk_prompt,
                    stream=False,
                )

                # -------- one-shot buffered --------
                answer = response.choices[0].message.content .strip() 
                return answer
            except Exception as e:
                return f"Error: {str(e)}"
  
        if _provider == "google":
            return google_process_query()
        if _provider == "openai" and _model in self.get_gpt_models_latest():
            return gpt_models_latest_process_query(self._gpt_models_latest_prev_resp_ids.get(self.get_session_id()))
        if _provider == "anthropic":
            return anthropic_process_query()
        return openai_sdk_process_query()


    def repair_python_cell(self, py_code: str) -> str:
            
        _CELL_REPAIR_RULES = """
        Fix the Python cell to satisfy:
        - Single valid cell; imports at the top.
        - Do not import or invoke or use 'python-dotenv' or 'dotenv' because it's not needed.
        - No top-level statements between if/elif/else branches.
        - Regression must use either sklearn with train_test_split (then X_test exists) and R^2/MAE/RMSE, 
            or statsmodels OLS. No accuracy_score in regression.
        - Keep all plotting + savefig + BytesIO + display inside the branch that created the figure. 
        - Return ONLY the corrected cell.
        """
        code = textwrap.dedent(py_code or "").strip()
        needs_fix = False
        if re.search(r"\baccuracy_score\b", code) and re.search(r"\bLinearRegression\b|\bOLS\b", code):
            needs_fix = True
        if re.search(r"\bX_test\b", code) and not re.search(r"\bX_test\s*=", code):
            needs_fix = True
        try:
            ast.parse(code)
        except SyntaxError:
            needs_fix = True
        if not needs_fix:
            return code
        _prompt = f"```python\n{code}\n```"
                  
        repair_profile = _prof.get_profile("vision2text") or _prof.get_profile("admin")
        if not repair_profile:
            return (
                '<div class="smx-alert smx-alert-warn">'
                    'No LLM profile configured for <code>coding</code> (or <code>admin</code>). <br>'
                    'Please, add the LLM profile inside the admin panel or contact your Administrator.'
                '</div>'
            )
        
        _client = _prof.get_client(repair_profile)
        _provider = repair_profile['provider'].lower()            
        _model = repair_profile['model']
        
        #1 Google
        if _provider == "google":
            from google.genai import types           
            
            fixed = _client.models.generate_content(
                model=_model,
                contents=_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=_CELL_REPAIR_RULES,
                    temperature=0.8,
                    max_output_tokens=1024,
                ),
            )
                    
        #2 Openai
        elif _provider == "openai" and _model in GPT_MODELS_LATEST:

            args = set_args(
                model=_model,
                instructions=_CELL_REPAIR_RULES,
                input=[{"role": "user", "content": _prompt}],
                previous_id=None,
                store=False,
                reasoning_effort="medium",
                verbosity="medium",
            )
            fixed = _out(_client.responses.create(**args))
    
        # Anthropic
        elif _provider == "anthropic":

            fixed = _client.messages.create(
                model=_model,
                max_tokens=1024,
                system=_CELL_REPAIR_RULES,
                messages=[{"role": "user", "content":_prompt}],
                stream=False,
            )  
                        
        # OpenAI SDK
        else:                 
            fixed = _client.chat.completions.create(
                model=_model,
                messages=[
                    {"role": "system", "content":_CELL_REPAIR_RULES},
                    {"role": "user", "content":_prompt},
                ],
                max_tokens=1024,
            )
                        
        try:
            ast.parse(fixed); 
            return fixed
        except Exception:
            return code

    def get_last_llm_usage(self):
        return getattr(self, "_last_llm_usage", None)

    def ai_generate_code(self, refined_question, tasks, df):

        def normalise_llm_code(s: str) -> str:
            s = s.replace("\t", "    ")
            s = textwrap.dedent(s)
            lines = s.splitlines()

            # drop leading blank lines
            while lines and not lines[0].strip():
                lines.pop(0)

            # if everything is still indented >=4 spaces, shift left
            indents = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
            if indents and min(indents) >= 4:
                m = min(indents)
                lines = [l[m:] if len(l) >= m else l for l in lines]

            return "\n".join(lines)
        
        CONTEXT = f"Columns: {list(df.columns)}\n\nDtypes: {df.dtypes.astype(str).to_dict()}\n\n"
        AVAILABLE_COLUMNS = list(df.columns)

        # --- SMX: normalise tasks coming from intent agent ---
        if isinstance(tasks, str):
            import json, ast, re
            try:
                tasks_parsed = json.loads(tasks)
            except Exception:
                try:
                    tasks_parsed = ast.literal_eval(tasks)
                except Exception:
                    tasks_parsed = re.findall(r"[A-Za-z_]+", tasks)
            tasks = tasks_parsed
        if not isinstance(tasks, list):
            tasks = [str(tasks)]
        tasks = [str(t).strip().lower() for t in tasks if str(t).strip()]

        ai_profile = """
        - You are a Python expert specializing in Data Science (DS) and Machine Learning (ML).
        - Your task is to generate a single, complete, production-quality, executable Python script for a Jupyter-like Python kernel, based on the given instructions. 
        - The dataset is already loaded as a pandas DataFrame named `df` (no file I/O or file uploads).
        - Make a copy of `df` and name it `df_copy`. 
        - Make sure `df_copy` is preprocessed and cleaned, and name it `df_cleaned`, if not already done so. 
        - Work only with `df_cleaned` to perform the ML tasks described in the given context.
        - Select your features and targets, from `df_cleaned`, with care and name it `required_cols`
        - Create your 'df_filtered by doing: df_filtered = df_cleaned[required_cols].
        - Use the {TEMPLATE_CATALOGUE} below to educate yourself on which visualizations you will implement in the code, and ensure the implementations are in the code you generate.
        - The final output MUST BE the complete, executable Python code only, enclosed in a single markdown code block (```python ... ```), and MUST BE able to fulfill the user's request: {tasks}.
        - Do not include any explanatory text or markdown outside the code block.
        """

        TEMPLATE_CATALOGUE = """
        ### Available SyntaxMatrix templates (use these instead of inventing new helpers)

        Visualisation templates:
        - viz_pie(df, category_col=None, top_k=8): pie/donut shares within a category.
        - viz_stacked_bar(df, x=None, hue=None, normalise=True): composition across groups.
        - viz_count_bar(df, category_col=None, top_k=12): counts/denominators by category.
        - viz_box(df, x=None, y=None): spread/outliers of numeric by category.
        - viz_scatter(df, x=None, y=None, hue=None): relationship between two numeric vars.
        - viz_distribution(df, col=None): histogram-style distribution for numeric.
        - viz_kde(df, col=None): density curve for numeric.
        - viz_area(df, time_col=None, y_col=None): area/trend over time.
        - viz_line(df, x=None, y=None, hue=None): line/trend plot.

        ML/stat templates:
        - classification(df): standard classification pipeline + metrics + plots.
        - regression(df): standard regression pipeline + metrics + plots.
        - clustering(df): clustering workflow + cluster plots.
        - anomaly_detection(df)
        - ts_anomaly_detection(df)
        - time_series_forecasting(df)
        - time_series_classification(df, entity_col, time_col, target_col)
        - dimensionality_reduction(df)
        - feature_selection(df)
        - eda_overview(df)
        - eda_correlation(df)
        - multilabel_classification(df, label_cols)
        - recommendation(df)
        - topic_modelling(df)
        """

        instructions = (
            "### Context"
            f"- DataFrame - (`df`): {df}"
            f"- Schema (names → dtypes): {CONTEXT}"
            f"- Row count: {len(df)}"
            f"- Task description: {refined_question}"
            f"- Tasks: {tasks}"
            f"- Available columns: {AVAILABLE_COLUMNS}"
            f"- Template catalogue: {TEMPLATE_CATALOGUE}"
            
            """
            ### Template rules
            - You MAY call 1 or more templates if they matche the task.
            - Do NOT invent template names.
            - If no template fits, write minimal direct pandas/sklearn/seaborn code instead, for visualization.
            - Keep the solution short: avoid writing wrappers/utilities already handled by SyntaxMatrix hardener.

            #### Template selection hint examples:
            - If the task asks for pie/donut/composition shares → use viz_pie.
            - If it asks for denominators/counts per category → viz_count_bar.
            - If it asks for spread/outliers/comparison across groups → viz_box.
            - If it asks for relationship / “X vs Y” → viz_scatter.
            - If it asks for trend over time → viz_line or viz_area.

            ### Hard requirements
            1) Code only. No markdown, no comments, no explanations.
            2) Import everything you use explicitly. 
            - Use pandas/numpy/matplotlib by default.
            - Seaborn may be unavailable at runtime; **do not import seaborn inside your code**.
            - If you call sns.*, assume sns is already defined by the framework.
            3) Avoid deprecated / removed APIs**, e.g.:
            - pandas: do not use `.append`, `.ix`, `.as_matrix`; prefer current patterns.
            - seaborn: do not use `distplot`; avoid `pairplot` on very large data unless sampling.
            - scikit-learn: import from `sklearn.model_selection` (not `sklearn.cross_validation`);
                set `random_state=42` where relevant.
            4) Be defensive, but avoid hard-failing on optional fields:
            - If the primary column, needed to answer the question, is missing, review your copy of the `df` again.
            - Make sure that you selected the proper column. Never use a column/variable which isn't available or defined.
            - If a secondary/extra column is missing, show a warning with `show(...)` and continue using available fields.
            - Handle missing values sensibly (drop rows for simple EDA; use `ColumnTransformer` + `SimpleImputer` for modelling).
            - For categorical features in ML, use `OneHotEncoder(handle_unknown="ignore")`
                inside a `Pipeline`/`ColumnTransformer` (no `LabelEncoder` on features).
            5) Keep it fast (kernel timeout ~8s):
            - For plots on large frames (>20k rows), downsample to ~1,000 rows
                (`df.sample(1000, random_state=42)`) unless aggregation is more appropriate.
            - Prefer vectorised ops; avoid O(n²) Python loops.
            6) Keep the solution compact:
            - Do not define large helper libraries or long “required column” sets.
            - Aim for ≤120 lines excluding imports.
            7) Always produce at least one visible result at the end:
            - If plotting with matplotlib/seaborn: call `plt.tight_layout(); plt.show()`.
            - If producing a table or metrics:
                `from syntaxmatrix.display import show` then `show(object_or_dataframe)`.
            8) Follow task type conventions:
            - **EDA/Stats**: compute the requested stat, then show a relevant table
                (e.g., summary/crosstab) or plot.
            - **Classification**: train/valid split (`train_test_split`), pipeline with scaling/encoding,
                fit, show accuracy and a confusion matrix via
                `ConfusionMatrixDisplay.from_estimator(...); plt.show()`.
                Also show `classification_report` as a dataframe if short.
            - **Regression**: train/valid split, pipeline as needed, fit, show R² and MAE;
                plot predicted vs actual scatter.
            - **Correlation/Chi-square/ANOVA**: compute the statistic + p-value and show a concise
                result table (with `show(...)`) and, when sensible, a small plot (heatmap/bar).
            9) Don't mutate or recreate target columns if they already exist.
            10) Keep variable names short and clear; prefer `num_cols` / `cat_cols` discovery by dtype.
            11) You MUST NOT reference any column outside Available columns: {AVAILABLE_COLUMNS}.
            12) If asked to predict/classify, choose the target by matching the task text to Allowed columns
                and never invent a new name.
            13) Treat df as the primary dataset you must work with.
            14) The dataset is already loaded as df (no file I/O or file uploads).
            15) All outputs must be visible to the user via the provided show(...) helper.
            16) Never use print(...); use show(...) instead.
            17) You MUST NOT read from or write to local files, folders, or external storage.
            - Do not call open(...), Path(...).write_text/write_bytes, or similar file APIs.
            - Do not use df.to_csv(...), df.to_excel(...), df.to_parquet(...),
                df.to_pickle(...), df.to_json(...), df.to_hdf(...), or any other
                method that writes to disk.
            - Do not call joblib.dump(...), pickle.dump(...), torch.save(...),
                numpy.save(...), numpy.savetxt(...), or similar saving functions.
            - Do not call plt.savefig(..., 'somefile.png') or any variant that
                writes an image to a filename. Plots must be rendered in-memory only.
            18) Keep everything in memory and surface results via show(...) or plots.
            
            #### Cohort rules
            When you generate plots for cohorts or categories, you MUST obey these rules:
            1) ALWAYS guard cohort masks:
            - After you define something like:
                _mask_a = (df['BMI'] < 18.5) & df['BMI'].notna()
                _mask_b = ~(df['BMI'] < 18.5) & df['BMI'].notna()
                compute their sizes:
                n_a = int(_mask_a.sum())
                n_b = int(_mask_b.sum())
            - If a mask has no rows (or almost none), do NOT draw an empty plot.
                Instead call:
                show(f"Skipping cohort '{label}': no rows after filtering.")
                and return.

            2) Before any groupby / crosstab for a plot:
            - Fill missing categories so groupby does not drop everything:
                df[col] = df[col].fillna("Unknown")
            - After building the table:
                tab = tmp.groupby([...]).size().unstack(...).fillna(0)
                ALWAYS check:
                if tab.empty:
                    show(f"Skipping plot for {col}: no data after grouping.")
                    continue
                Only call .plot(...) if the table is non-empty.

            3) For value_counts-based plots:
            - If the Series is empty after filtering (len(s) == 0),
                do NOT draw a figure. Just call:
                show(f"No data available to plot for {col} in this cohort.")
                and skip.

            4) Never try to “hide” an error with a blank plot.
            A blank chart is treated as a bug. If there is no data, explain it
            clearly using show(...), and avoid calling matplotlib/Seaborn.

            5) Never use print(...). All user-visible diagnostics go through show(...).

                
            ### Output
            Return only runnable Python that:
            - Imports what it needs,
            - Validates columns,
            - Visualize tables, charts, and graphs, each with appropriate caption.
            - Solution: {tasks} to solve {refined_question},
            - And ends with at least 3 visible output (`show(...)` and/or `plt.show()`).
        """)

        if not self._coding_profile:
            coding_profile = _prof.get_profile("coding") or _prof.get_profile("admin")
            if not coding_profile:
                return (
                    '<div class="smx-alert smx-alert-warn">'
                        'No LLM profile configured for <code>coding</code> (or <code>admin</code>). <br>'
                        'Please, add the LLM profile inside the admin panel or contact your Administrator.'
                    '</div>'
                )

            self._coding_profile = coding_profile
            self._coding_profile['client'] = _prof.get_client(coding_profile)

        # code = mlearning_agent(instructions, ai_profile, self._coding_profile)
        code, usage = mlearning_agent(instructions, ai_profile, self._coding_profile)
        self._last_llm_usage = usage

        if code:
            import re
            code = normalise_llm_code(code)

            m = re.search(r"```(?:python)?\s*(.*?)\s*```", code, re.DOTALL | re.IGNORECASE)
            if m:
                code = m.group(1).strip()

            if "import io" not in code and "io.BytesIO" in code:
                lines = code.split('\n')
                import_lines = []
                other_lines = []

                for line in lines:
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_lines.append(line)
                    else:
                        other_lines.append(line)

                if "import io" not in '\n'.join(import_lines):
                    import_lines.append('import io')

                code = '\n'.join(import_lines + [''] + other_lines)

                TEMPLATE_NAMES = [
                    "viz_pie","viz_stacked_bar","viz_count_bar","viz_box","viz_scatter",
                    "viz_distribution","viz_kde","viz_area","viz_line",
                    "classification","regression","clustering","anomaly_detection",
                    "ts_anomaly_detection","time_series_forecasting","time_series_classification",
                    "dimensionality_reduction","feature_selection","eda_overview","eda_correlation",
                    "multilabel_classification","recommendation","topic_modelling"
                ]

                used = [t for t in TEMPLATE_NAMES if re.search(rf"\\b{t}\\s*\\(", code)]
                if used:
                    import_line = (
                        "from syntaxmatrix.agentic.model_templates import " +
                        ", ".join(sorted(set(used)))
                    )
                    if import_line not in code:
                        code = import_line + "\n" + code

            return code.strip()

        return "Error: AI code generation failed."


    def sanitize_rough_to_markdown_task(self, rough: str) -> str:
        """
        Return only the Task text (no tags).
        Behaviour:
        - If <Task>...</Task> exists: return its inner text.
        - If not: return the input with <rough> wrapper and any <Error> blocks removed.
        - Never raises; always returns a string.
        """
        s = ("" if rough is None else str(rough)).strip()

        def _find_ci(hay, needle, start=0):
            return hay.lower().find(needle.lower(), start)

        # Prefer explicit <Task>...</Task>
        i = _find_ci(s, "<task")
        if i != -1:
            j = s.find(">", i)
            k = _find_ci(s, "</task>", j + 1)
            if j != -1 and k != -1:
                return s[j + 1:k].strip()
        # Otherwise strip any <Error>...</Error> blocks (if present)
        out = s
        while True:
            e1 = _find_ci(out, "<error")
            if e1 == -1:
                break
            e1_end = out.find(">", e1)
            e2 = _find_ci(out, "</error>", (e1_end + 1) if e1_end != -1 else e1 + 1)
            if e1_end == -1 or e2 == -1:
                break
            out = out[:e1] + out[e2 + len("</error>"):]

        # Drop optional <rough> wrapper
        return out.replace("<rough>", "").replace("</rough>", "").strip()


    def run(self):
        url = f"http://{self.host}:{self.port}/"
        webbrowser.open(url)
        self.app.run(host=self.host, port=self.port, debug=False)
