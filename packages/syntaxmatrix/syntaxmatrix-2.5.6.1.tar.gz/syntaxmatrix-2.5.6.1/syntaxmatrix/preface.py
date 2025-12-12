# === SMX Auto-Hardening Preface (do not edit) ===
import warnings, numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
from sklearn.preprocessing import OneHotEncoder
import inspect
import pandas as _pd
import numpy as _np  # noqa: F811

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)

__all__ = [
    # plotting entrypoints
    "SB_histplot",
    "SB_barplot",
    "SB_boxplot",
    "SB_scatterplot",
    "SB_heatmap",

    # core helpers (all underscore-prefixed functions)
    "_SMX_caption_from_ctx",
    "_SMX_axes_have_titles",
    "_SMX_export_png",
    "_pick_df",
    "_pick_ax_slot",
    "_first_numeric",
    "_first_categorical",
    "_safe_plot",
    "_safe_concat",
    "_SMX_OHE",
    "_SMX_mm",
    "_SMX_call",
    "_SMX_rmse",
    "_SMX_autocoerce_dates",
    "_SMX_autocoerce_numeric",

    # display helper
    "smx_show",
    "show",

    # metics
    "r2_score",
    "mean_absolute_error",
    "accuracy_score",
    "precision_score",
    "recall_score",
    "f1_score",
    "roc_auc_score",
    "confusion_matrix",
    "ConfusionMatrixDisplay",
    "classification_report",
]


try:
    import seaborn as sns
except Exception:
    class _Dummy:
        def __getattr__(self, name):
            def _f(*a, **k):
                from syntaxmatrix.display import show
                show('⚠ seaborn not available; plot skipped.')
            return _f
    sns = _Dummy()

from syntaxmatrix.display import show as _SMX_base_show


boxplot = barplot = histplot = distplot = lineplot = countplot = heatmap = pairplot = None


def smx_show(obj, title=None):
    try:
        import pandas as pd, numbers
        cap = (title or _SMX_caption_from_ctx())
        # 1) DataFrame → Styler with caption
        if isinstance(obj, pd.DataFrame):
            try:
                return _SMX_base_show(obj.style.set_caption(cap))
            except Exception:
                pass
        # 2) dict of scalars → DataFrame with caption
        if isinstance(obj, dict) and all(isinstance(v, numbers.Number) for v in obj.values()):
            df_ = pd.DataFrame({'metric': list(obj.keys()), 'value': list(obj.values())})
            try:
                return _SMX_base_show(df_.style.set_caption(cap))
            except Exception:
                return _SMX_base_show(df_)
    except Exception:
        pass
    return _SMX_base_show(obj)


def _SMX_caption_from_ctx():
    """
    Look up refined_question / askai_question in caller frames,
    falling back to 'Table' if not found.
    """
    import inspect

    frame = inspect.currentframe()
    while frame is not None:
        g = frame.f_globals
        t = g.get("refined_question") or g.get("askai_question")
        if t:
            return str(t).strip().splitlines()[0][:120]
        frame = frame.f_back

    return "Table"


def _SMX_axes_have_titles(fig=None):
    import matplotlib.pyplot as _plt
    fig = fig or _plt.gcf()
    try:
        for _ax in fig.get_axes():
            if (_ax.get_title() or '').strip():
                return True
    except Exception:
        pass
    return False


def _SMX_export_png():
    import io, base64
    fig = plt.gcf()
    try:
        if not _SMX_axes_have_titles(fig):
            fig.suptitle(_SMX_caption_from_ctx(), fontsize=10)
    except Exception:
        pass
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    from IPython.display import display, HTML
    _img = base64.b64encode(buf.read()).decode('ascii')
    display(
        HTML(
            f"<img src='data:image/png;base64,{_img}' "
            "style='max-width:100%;height:auto;border:1px solid #ccc;border-radius:4px;'/>"
        )
    )
    plt.close()


def _pick_df():
    """
    Try to find `df` in the caller's context, not just this module.
    This restores the behaviour we had when the preface lived inline.
    """
    import inspect

    # 1) Check our own module globals first (just in case).
    g = globals()
    if "df" in g:
        return g["df"]

    # 2) Walk up the call stack looking for `df`
    frame = inspect.currentframe().f_back
    while frame is not None:
        # locals of the frame
        if "df" in frame.f_locals:
            return frame.f_locals["df"]
        # globals of the frame (e.g. the exec cell)
        if "df" in frame.f_globals:
            return frame.f_globals["df"]
        frame = frame.f_back

    return None


def _pick_ax_slot():
    ax = None
    try:
        _axes = globals().get('axes', None)
        import numpy as _np
        if _axes is not None:
            arr = _np.ravel(_axes)
            for _a in arr:
                try:
                    if hasattr(_a, 'has_data') and not _a.has_data():
                        ax = _a
                        break
                except Exception:
                    continue
    except Exception:
        ax = None
    return ax


def _first_numeric(_d):
    import numpy as np, pandas as pd
    try:
        preferred = ["median_house_value", "price", "value", "target", "label", "y"]
        for c in preferred:
            if c in _d.columns and pd.api.types.is_numeric_dtype(_d[c]):
                return c
        cols = _d.select_dtypes(include=[np.number]).columns.tolist()
        return cols[0] if cols else None
    except Exception:
        return None


def _first_categorical(_d):
    import pandas as pd, numpy as np
    try:
        num = set(_d.select_dtypes(include=[np.number]).columns.tolist())
        cand = [c for c in _d.columns if c not in num and _d[c].nunique(dropna=True) <= 50]
        return cand[0] if cand else None
    except Exception:
        return None


def _safe_plot(func, *args, **kwargs):
    try:
        ax = func(*args, **kwargs)
        if ax is None:
            ax = plt.gca()
        try:
            if hasattr(ax, 'has_data') and not ax.has_data():
                from syntaxmatrix.display import show as _show
                _show('⚠ Empty plot: no data drawn.')
        except Exception:
            pass
        try:
            plt.tight_layout()
        except Exception:
            pass
        return ax
    except Exception as e:
        from syntaxmatrix.display import show as _show
        _show(f'⚠ Plot skipped: {type(e).__name__}: {e}')
        return None


def SB_histplot(*a, **k):
    _missing = (getattr(sns, '__class__', type(sns)).__name__ == '_Dummy')
    _sentinel = (len(a) >= 1 and a[0] is None)
    if (not a or _sentinel) and not k:
        d = _pick_df()
        if d is not None:
            x = _first_numeric(d)
            if x is not None:
                def _draw():
                    plt.hist(d[x].dropna())
                    ax = plt.gca()
                    if not (ax.get_title() or '').strip():
                        ax.set_title(f'Distribution of {x}')
                    return ax
                return _safe_plot(lambda **kw: _draw())
    if _missing:
        return _safe_plot(lambda **kw: plt.hist([]))
    if _sentinel:
        a = a[1:]
    return _safe_plot(getattr(sns, 'histplot', plt.hist), *a, **k)


def SB_barplot(*a, **k):
    _missing = (getattr(sns, '__class__', type(sns)).__name__ == '_Dummy')
    _sentinel = (len(a) >= 1 and a[0] is None)
    _ax = k.get('ax') or _pick_ax_slot()
    if _ax is not None:
        try:
            plt.sca(_ax)
        except Exception:
            pass
        k.setdefault('ax', _ax)
    if (not a or _sentinel) and not k:
        d = _pick_df()
        if d is not None:
            x = _first_categorical(d)
            y = _first_numeric(d)
            if x and y:
                import pandas as _pd
                g = d.groupby(x)[y].mean().reset_index()

                def _draw():
                    if _missing:
                        plt.bar(g[x], g[y])
                    else:
                        sns.barplot(data=g, x=x, y=y, ax=k.get('ax'))
                    ax = plt.gca()
                    if not (ax.get_title() or '').strip():
                        ax.set_title(f'Mean {y} by {x}')
                    return ax

                return _safe_plot(lambda **kw: _draw())
    if _missing:
        return _safe_plot(lambda **kw: plt.bar([], []))
    if _sentinel:
        a = a[1:]
    return _safe_plot(sns.barplot, *a, **k)


def SB_boxplot(*a, **k):
    _missing = (getattr(sns, '__class__', type(sns)).__name__ == '_Dummy')
    _sentinel = (len(a) >= 1 and a[0] is None)
    _ax = k.get('ax') or _pick_ax_slot()
    if _ax is not None:
        try:
            plt.sca(_ax)
        except Exception:
            pass
        k.setdefault('ax', _ax)
    if (not a or _sentinel) and not k:
        d = _pick_df()
        if d is not None:
            x = _first_categorical(d)
            y = _first_numeric(d)
            if x and y:
                def _draw():
                    if _missing:
                        plt.boxplot(d[y].dropna())
                    else:
                        sns.boxplot(data=d, x=x, y=y, ax=k.get('ax'))
                    ax = plt.gca()
                    if not (ax.get_title() or '').strip():
                        ax.set_title(f'Distribution of {y} by {x}')
                    return ax

                return _safe_plot(lambda **kw: _draw())
    if _missing:
        return _safe_plot(lambda **kw: plt.boxplot([]))
    if _sentinel:
        a = a[1:]
    return _safe_plot(sns.boxplot, *a, **k)


def SB_scatterplot(*a, **k):
    _missing = (getattr(sns, '__class__', type(sns)).__name__ == '_Dummy')
    fn = getattr(sns, 'scatterplot', None)
    # If seaborn is unavailable OR the caller passed (data=..., x='col', y='col'),
    # use a robust matplotlib path that looks up data and coerces to numeric.
    if _missing or fn is None:
        data = k.get('data')
        x = k.get('x')
        y = k.get('y')
        if (
            data is not None
            and isinstance(x, str)
            and isinstance(y, str)
            and x in data.columns
            and y in data.columns
        ):
            xs = pd.to_numeric(data[x], errors='coerce')
            ys = pd.to_numeric(data[y], errors='coerce')
            m = xs.notna() & ys.notna()

            def _draw():
                plt.scatter(xs[m], ys[m])
                ax = plt.gca()
                if not (ax.get_title() or '').strip():
                    ax.set_title(f'{y} vs {x}')
                return ax

            return _safe_plot(lambda **kw: _draw())
        # else: fall back to auto-pick two numeric columns
        d = _pick_df()
        if d is not None:
            num = d.select_dtypes(include=[np.number]).columns.tolist()
            if len(num) >= 2:
                def _draw2():
                    plt.scatter(d[num[0]], d[num[1]])
                    ax = plt.gca()
                    if not (ax.get_title() or '').strip():
                        ax.set_title(f'{num[1]} vs {num[0]}')
                    return ax

                return _safe_plot(lambda **kw: _draw2())
        return _safe_plot(lambda **kw: plt.scatter([], []))
    # seaborn path
    return _safe_plot(fn, *a, **k)


def SB_heatmap(*a, **k):
    _missing = (getattr(sns, '__class__', type(sns)).__name__ == '_Dummy')
    data = None
    if a:
        data = a[0]
    elif 'data' in k:
        data = k['data']
    if data is None:
        d = _pick_df()
        try:
            if d is not None:
                import numpy as _np
                data = d.select_dtypes(include=[_np.number]).corr()
        except Exception:
            data = None
    if data is None:
        from syntaxmatrix.display import show as _show
        _show('⚠ Heatmap skipped: no data.')
        return None
    if not _missing and hasattr(sns, 'heatmap'):
        _k = {kk: vv for kk, vv in k.items() if kk != 'data'}

        def _draw():
            ax = sns.heatmap(data, **_k)
            try:
                ax = ax or plt.gca()
                if not (ax.get_title() or '').strip():
                    ax.set_title('Correlation Heatmap')
            except Exception:
                pass
            return ax

        return _safe_plot(lambda **kw: _draw())

    def _mat_heat():
        im = plt.imshow(data, aspect='auto')
        try:
            plt.colorbar()
        except Exception:
            pass
        try:
            cols = list(getattr(data, 'columns', []))
            rows = list(getattr(data, 'index', []))
            if cols:
                plt.xticks(range(len(cols)), cols, rotation=90)
            if rows:
                plt.yticks(range(len(rows)), rows)
        except Exception:
            pass
        ax = plt.gca()
        try:
            if not (ax.get_title() or '').strip():
                ax.set_title('Correlation Heatmap')
        except Exception:
            pass
        return ax

    return _safe_plot(lambda **kw: _mat_heat())


def _safe_concat(objs, **kwargs):
    import pandas as _pd
    if objs is None:
        return _pd.DataFrame()
    if isinstance(objs, (list, tuple)) and len(objs) == 0:
        return _pd.DataFrame()
    try:
        return _pd.concat(objs, **kwargs)
    except Exception as e:
        smx_show(f'⚠ concat skipped: {e}')
        return _pd.DataFrame()
    

def _SMX_OHE(**k):
    # normalise arg name across sklearn versions
    if "sparse" in k and "sparse_output" not in k:
        k["sparse_output"] = k.pop("sparse")
    k.setdefault("handle_unknown", "ignore")
    k.setdefault("sparse_output", False)
    try:
        if "sparse_output" not in inspect.signature(OneHotEncoder).parameters:
            if "sparse_output" in k:
                k["sparse"] = k.pop("sparse_output")
        return OneHotEncoder(**k)
    except TypeError:
        if "sparse_output" in k:
            k["sparse"] = k.pop("sparse_output")
        return OneHotEncoder(**k)
        

def _SMX_mm(a, b):
    try:
        return a @ b  # normal path
    except Exception:
        try:
            A = _np.asarray(a)
            B = _np.asarray(b)
            # If same 2D shape (e.g. (n,k) & (n,k)), treat as row-wise dot
            if A.ndim == 2 and B.ndim == 2 and A.shape == B.shape:
                return (A * B).sum(axis=1)
            # Otherwise try element-wise product (broadcast if possible)
            return A * B
        except Exception as e:
            smx_show(f'⚠ Matmul relaxed: {type(e).__name__}: {e}')
            return _np.nan


def _SMX_call(fn, *a, **k):
    try:
        return fn(*a, **k)
    except TypeError as e:
        msg = str(e)
        if "unexpected keyword argument 'squared'" in msg:
            k.pop('squared', None)
            return fn(*a, **k)
        raise


def _SMX_rmse(y_true, y_pred):
    try:
        from sklearn.metrics import mean_squared_error as _mse
        try:
            return _mse(y_true, y_pred, squared=False)
        except TypeError:
            return (_mse(y_true, y_pred)) ** 0.5
    except Exception:
        import numpy as _np
        yt = _np.asarray(y_true, dtype=float)
        yp = _np.asarray(y_pred, dtype=float)
        diff = yt - yp
        return float((_np.mean(diff * diff)) ** 0.5)


def _SMX_autocoerce_dates(_df):
    if _df is None or not hasattr(_df, 'columns'):
        return
    for c in list(_df.columns):
        s = _df[c]
        n = str(c).lower()
        if _pd.api.types.is_datetime64_any_dtype(s):
            continue
        if (
            _pd.api.types.is_object_dtype(s)
            or ('date' in n or 'time' in n or 'timestamp' in n or n.endswith('_dt'))
        ):
            try:
                conv = _pd.to_datetime(s, errors='coerce', utc=True).dt.tz_localize(None)
                # accept only if at least 10% (min 3) parse as dates
                if getattr(conv, 'notna', lambda: _pd.Series([]))().sum() >= max(3, int(0.1 * len(_df))):
                    _df[c] = conv
            except Exception:
                pass


def _SMX_autocoerce_numeric(_df, cols):
    if _df is None:
        return
    for c in cols:
        if c in getattr(_df, 'columns', []):
            try:
                _df[c] = _pd.to_numeric(_df[c], errors='coerce')
            except Exception:
                pass

def show(*args, **kwargs):
    return smx_show(*args, **kwargs)