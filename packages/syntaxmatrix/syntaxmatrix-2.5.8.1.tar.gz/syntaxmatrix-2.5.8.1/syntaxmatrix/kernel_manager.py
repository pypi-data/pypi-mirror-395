# kernel_manager.py

import jupyter_client
import nest_asyncio
import io, contextlib
import time   
from functools import wraps
import inspect, pandas as _pd
from functools import wraps
import inspect, pandas as _pd
import io, contextlib
import html as _html
import re as _re

nest_asyncio.apply()

class SyntaxMatrixKernelManager:
    _kernels = {}

    @classmethod
    def start_kernel(cls, session_id):
        if session_id in cls._kernels:
            return cls._kernels[session_id]
        km = jupyter_client.KernelManager()
        km.start_kernel()
        kc = km.client()
        kc.start_channels()
        cls._kernels[session_id] = (km, kc)
        return km, kc

    @classmethod
    def get_kernel(cls, session_id):
        return cls._kernels.get(session_id, (None, None))

    @classmethod
    def shutdown_kernel(cls, session_id):
        km, kc = cls._kernels.pop(session_id, (None, None))
        if kc:
            kc.stop_channels()
        if km:
            km.shutdown_kernel(now=True)

    @classmethod
    def cleanup_all(cls):
        for sid in list(cls._kernels):
            cls.shutdown_kernel(sid)


_df_cache = None

def execute_code_in_kernel(kc, code, timeout=120):

    _local_stdout = ""
    _local_stderr = ""

    global _df_cache
    exec_namespace = {}

    if not hasattr(_pd.core.generic.NDFrame, "_patch_safe_reduce"):
        _AGG_FUNCS = (
            "sum", "mean", "median", "std", "var",
            "min", "max", "prod",
        )

        def _make_wrapper(name):
            orig = getattr(_pd.core.generic.NDFrame, name)

            @wraps(orig)
            def _wrapper(self, *args, **kwargs):
                try:
                    return orig(self, *args, **kwargs)

                except TypeError as exc:
                    msg = str(exc)
                    if (
                        "can only concatenate str" not in msg
                        and "could not convert"   not in msg
                    ):
                        raise  # - not the error we’re guarding against

                    # Caller already supplied numeric_only (positional or kw) → re-raise
                    if len(args) >= 3 or "numeric_only" in kwargs:
                        raise

                    kwargs = dict(kwargs)
                    kwargs["numeric_only"] = True
                    return orig(self, *args, **kwargs)

            return _wrapper

        for _fn in _AGG_FUNCS:
            setattr(
                _pd.core.generic.NDFrame,
                f"_orig_{_fn}",
                getattr(_pd.core.generic.NDFrame, _fn),
            )
            setattr(
                _pd.core.generic.NDFrame,
                _fn,
                _make_wrapper(_fn),
            )

        # marker so we don’t patch twice in the same kernel
        _pd.core.generic.NDFrame._patch_safe_reduce = True

    if "_pandas_sum_patched" not in exec_namespace:

        if not hasattr(_pd.core.generic.NDFrame, "_orig_sum"):
            _pd.core.generic.NDFrame._orig_sum  = _pd.core.generic.NDFrame.sum
            _pd.core.generic.NDFrame._orig_mean = _pd.core.generic.NDFrame.mean   # ← NEW

            def _safe_agg(orig_func):
                def wrapper(self, *args, **kwargs):
                    try:
                        return orig_func(self, *args, **kwargs)

                    except TypeError as exc:
                        # Only rescue the classic mixed-dtype failure
                        if ("can only concatenate"   not in str(exc) and
                            "could not convert"      not in str(exc)):
                            raise

                        # Caller already gave numeric_only → we must not override
                        if "numeric_only" in kwargs or len(args) >= 3:
                            raise

                        kwargs = dict(kwargs)
                        kwargs["numeric_only"] = True
                        return orig_func(self, *args, **kwargs)
                return wrapper

            _pd.core.generic.NDFrame.sum  = _safe_agg(_pd.core.generic.NDFrame._orig_sum)
            _pd.core.generic.NDFrame.mean = _safe_agg(_pd.core.generic.NDFrame._orig_mean)

        exec_namespace["_pandas_sum_patched"] = True

    # inject cached df if we have one
    if _df_cache is not None:
        exec_namespace["df"] = _df_cache
    
    try:
        # Prevent any print()/stdout/stderr from hitting your server console
        _buf_out, _buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(_buf_out), contextlib.redirect_stderr(_buf_err):
            exec(code, exec_namespace, exec_namespace)
        
        _local_stdout = _buf_out.getvalue()
        _local_stderr = _buf_err.getvalue()

    # ── show a friendly “missing package” hint ────
    except (ModuleNotFoundError, ImportError) as e:
        missing = getattr(e, "name", None) or str(e).split("'")[1]
        hint = (

            f"<div style='color:red; font-weight:bold;'>"
            f"Missing package: <code>{missing}</code><br>"
            f"Activate this virtual-env and run:<br>"
            f"<code>pip install {missing}</code><br>"
            f"then re-run your query.</div>"
        )
        return [hint], []      
    
    except Exception:
        pass

   # cache df for next call
    if "df" in exec_namespace:
        _df_cache = exec_namespace["df"]

    # Auto-import display if needed (original code) :contentReference[oaicite:0]{index=0}
    if "display(" in code and "from IPython.display import display" not in code:
        code = "from IPython.display import display\n" + code

    # ------------------------------------------------------------------
    # everything below is the original while-loop message collector
    msg_id = kc.execute(
        code,
        user_expressions={"_last": "(_)",},
        allow_stdin=False,
    )
    output_blocks, errors = [], []
    start_time = time.time()

    while True:
        # Block until a message is available; if `timeout` is None this will block.
        try:
            msg = kc.get_iopub_msg(timeout=timeout)
        except Exception:
            break   # only trips if a numeric timeout was provided                             # timeout reached

        if msg["parent_header"].get("msg_id") != msg_id:
            continue

        mtype, content = msg["msg_type"], msg["content"]
        # Stop cleanly when the kernel reports it is idle (execution finished)        
        if mtype == 'status' and content.get('execution_state') == 'idle':
            break

        # if mtype == "stream":
        #     output_blocks.append(f"<pre>{content['text']}</pre>")

        if mtype == "stream":
            raw = content.get("text", "")
            # Remove noisy reprs from printed HTML/Markdown display objects
            lines = [
                ln for ln in raw.splitlines()
                if ("IPython.core.display.HTML object" not in ln
                    and "IPython.core.display.Markdown object" not in ln)
            ]
            txt = "\n".join(lines).strip()
            if txt:
                output_blocks.append(f"<pre>{_html.escape(txt)}</pre>")

        # elif mtype in ("execute_result", "display_data"):
        #     data = content["data"]
        #     if "text/html" in data:
        #         output_blocks.append(data["text/html"])
        #     elif "image/png" in data:
        #         output_blocks.append(
        #             f"<img src='data:image/png;base64,{data['image/png']}' "
        #             f"style='max-width:100%;'/>"
        #         )
        #     else:
        #         output_blocks.append(f"<pre>{data.get('text/plain','')}</pre>")

        elif mtype in ("execute_result", "display_data"):
            data = content.get("data", {})
            if "text/html" in data:
                 output_blocks.append(data["text/html"])
            elif "image/png" in data:
                 output_blocks.append(
                     f"<img src='data:image/png;base64,{data['image/png']}' "
                     f"style='max-width:100%;'/>"
                 )
       
            else:
                 # Clean up plain-text reprs like "<IPython.core.display.HTML object>"
                txt = data.get("text/plain", "") or ""
                if ("IPython.core.display.HTML object" in txt
                    or "IPython.core.display.Markdown object" in txt):
                    # skip useless reprs entirely
                    continue
                output_blocks.append(f"<pre>{_html.escape(txt)}</pre>")

        elif mtype == "error":
            # keep the traceback html-friendly
            traceback_html = "<br>".join(content["traceback"])
            errors.append(f"<pre style='color:red;'>{traceback_html}</pre>")
    # --- surface the locally captured commentary (stdout/stderr) back to the UI ---
    if _local_stdout.strip():
        # Put commentary first so the user sees it above plots/tables
        output_blocks.insert(0, f"<pre>{_html.escape(_local_stdout)}</pre>")
    if _local_stderr.strip():
        errors.insert(0, f"<pre style='color:#b00;'>{_html.escape(_local_stderr)}</pre>")

    def _smx_strip_display_reprs(text: str) -> str:
        if not text:
            return text
        # remove tokens like "<IPython.core.display.HTML object>"
        text = _re.sub(r"<IPython\.core\.display\.[A-Za-z]+\s+object>", "", text)
        # if these were printed as lists, remove leftover brackets/commas
        text = _re.sub(r"[\[\],]", " ", text)
        # collapse whitespace
        text = _re.sub(r"\s+", " ", text).strip()
        return text

    _cleaned_blocks = []
    for blk in output_blocks:
        # pre-wrapped plaintext
        if blk.startswith("<pre>") and blk.endswith("</pre>"):
            inner = blk[5:-6]
            inner = _smx_strip_display_reprs(_html.unescape(inner))
            if inner:
                _cleaned_blocks.append(f"<pre>{_html.escape(inner)}</pre>")
            # if empty after cleaning, drop it
            continue

        # html/img payloads: just remove stray repr tokens if they slipped in
        cleaned = _re.sub(r"<IPython\.core\.display\.[A-Za-z]+\s+object>", "", blk)
        _cleaned_blocks.append(cleaned)
    output_blocks = _cleaned_blocks

    return output_blocks, errors