"""
syntaxmatrix.display
--------------------
Single responsibility: render arbitrary Python objects in the SMX UI.

- Matplotlib figures: displayed directly.
- Pandas Styler (with .set_caption): rendered to HTML so captions always show.
- Pandas DataFrame/Series: rendered to HTML (no caption path).
- Dict of scalars: rendered as a small table.
- Tuple of two numbers (e.g., mse, r2): rendered as a labelled 2-row table.
- Everything else: shown as <pre> for safe inspection.
"""

from typing import Any
import numbers

import pandas as pd
import matplotlib.figure as mpfig
from IPython.display import display, HTML

try:
    # Optional: if pandas Styler exists, we can keep captions reliably
    from pandas.io.formats.style import Styler as _Styler  # type: ignore
except Exception:  # pragma: no cover
    _Styler = None  # type: ignore


__all__ = ["show"]


# ---- internal helpers -------------------------------------------------------


def _wrap_html_table(html: str) -> str:
    """Apply consistent UI styling and horizontal scrolling."""
    return (
        "<style>"
        "caption{caption-side: top; font-weight:600; margin:0 0 6px 0;}"
        "table{border-collapse:collapse;font-size:0.9em;white-space:nowrap;}"
        "th{background:#f0f2f5;text-align:left;padding:6px 8px;border:1px solid gray;}"
        "td{border:1px solid #ddd;padding:6px 8px;}"
        "tbody tr:nth-child(even){background-color:#f9f9f9;}"
        "</style>"
        "<div style='overflow-x:auto;max-width:100%;margin-bottom:1rem;'>"
        + html +
        "</div>"
    )


# ---- public API -------------------------------------------------------------


def show(obj: Any) -> None:
    """
    Render common objects so the Dashboard (or chat) always shows output.

    Notes
    -----
    * Do not print here. All rendering goes through IPython's display layer.
    * Captions are supplied upstream by the SMX PREFACE via DataFrame.style.set_caption(...).
    """
    # 1) Matplotlib figures
    if isinstance(obj, mpfig.Figure):
        display(obj)
        return None

    # 2) Pandas Styler (keeps caption)
    if _Styler is not None and isinstance(obj, _Styler):  # type: ignore
        try:
            html = obj.to_html()
            display(HTML(_wrap_html_table(html)))
        except Exception:
            # Fallback: if Styler HTML fails for any reason, display raw Styler
            display(obj)
        return None

    # 3) Series / DataFrame (no caption path)
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        html = obj.to_html(classes="smx-table", border=0)
        display(HTML(_wrap_html_table(html)))
        return None

    # 4) Dict of scalar numbers → pretty 2-col table
    if isinstance(obj, dict) and all(isinstance(v, numbers.Number) for v in obj.values()):
        df_ = pd.DataFrame({"metric": list(obj.keys()), "value": list(obj.values())})
        html = df_.to_html(classes="smx-table", border=0, index=False)
        display(HTML(_wrap_html_table(html)))
        return None

    # 5) Two-number tuple → labelled metric table (e.g., (mse, r2))
    if (
        isinstance(obj, tuple)
        and len(obj) == 2
        and all(isinstance(v, numbers.Number) for v in obj)
    ):
        mse, r2 = obj
        df_ = pd.DataFrame(
            {"metric": ["Mean-squared error", "R²"], "value": [mse, r2]}
        )
        html = df_.to_html(classes="smx-table", border=0, index=False)
        display(HTML(_wrap_html_table(html)))
        return None

    # 6) Fallback: show as preformatted text (safe and predictable)
    display(HTML(f"<pre>{obj}</pre>"))
    return None
