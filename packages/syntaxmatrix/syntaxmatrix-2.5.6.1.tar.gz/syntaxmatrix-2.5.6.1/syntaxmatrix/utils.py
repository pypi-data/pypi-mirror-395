from __future__ import annotations
import re, textwrap
import pandas as pd
import numpy as np
import warnings

from difflib import get_close_matches
from typing import Iterable, Tuple, Dict
import inspect
from sklearn.preprocessing import OneHotEncoder


from syntaxmatrix.agentic.model_templates import (
    classification, regression, multilabel_classification,
    eda_overview, eda_correlation,
    anomaly_detection, ts_anomaly_detection,
    dimensionality_reduction, feature_selection,
    time_series_forecasting, time_series_classification,
    unknown_group_proxy_pack, viz_line,
    clustering, recommendation, topic_modelling,
    viz_pie, viz_count_bar, viz_box, viz_scatter,
    viz_stacked_bar, viz_distribution, viz_area, viz_kde,
)
import ast

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

INJECTABLE_INTENTS = [
    "classification",
    "multilabel_classification",
    "regression",
    "anomaly_detection",
    "time_series_forecasting",
    "time_series_classification",
    "ts_anomaly_detection",
    "dimensionality_reduction",
    "feature_selection",
    "clustering",
    "eda",
    "correlation_analysis",
    "visualisation",
    "recommendation",
    "topic_modelling",
]

def classify_ml_job(prompt: str) -> str:
    """
    Very-light intent classifier.
    Returns one of:
      'stat_test' | 'time_series' | 'clustering'
      'classification' | 'regression' | 'eda'
    """
    p = prompt.lower()

    greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings"}
    if any(p.startswith(g) or p == g for g in greetings):
        return "greeting"

    # Feature selection / importance intent
    if any(k in p for k in (
        "feature selection", "select k best", "selectkbest", "rfe",
        "mutual information", "feature importance", "permutation importance",
        "feature engineering suggestions"
    )):
        return "feature_selection"

    # Dimensionality reduction intent
    if any(k in p for k in (
        "pca", "principal component", "dimensionality reduction",
        "reduce dimension", "reduce dimensionality", "t-sne", "tsne", "umap"
        )):
        return "dimensionality_reduction"

    # Anomaly / outlier intent
    if any(k in p for k in (
        "anomaly", "anomalies", "outlier", "outliers", "novelty",
        "fraud", "deviation", "rare event", "rare events", "odd pattern",
        "suspicious"
        )):
        return "anomaly_detection"

    if any(k in p for k in ("t-test", "anova", "p-value")):
        return "stat_test"
    if "forecast" in p or "prophet" in p:
        return "time_series"
    if "cluster" in p or "kmeans" in p:
        return "clustering"
    if any(k in p for k in ("accuracy", "precision", "roc")):
        return "classification"
    if any(k in p for k in ("rmse", "r2", "mae")):
        return "regression"
    
    return "eda"


def _indent(code: str, spaces: int = 4) -> str:
    """
    Indent a block of code by `spaces` spaces, line by line.
    Blank lines are preserved unchanged.
    """
    pad = " " * spaces
    lines = code.splitlines()
    return "\n".join((pad + line) if line.strip() else line for line in lines)


def wrap_llm_code_safe(body: str) -> str:
    """
    Wrap arbitrary LLM code so that:
      - Any exception is caught and shown.
      - A minimal, useful EDA fallback still runs so the user sees *something*.
    This happens once in the framework; you never touch the individual cells.
    """
    return textwrap.dedent(
        "try:\n"
        + _indent(body)
        + "\n"
        "except Exception as e:\n"
        "    from syntaxmatrix.display import show\n"
        "    msg = f\"⚠️ Skipped LLM block due to: {type(e).__name__}: {e}\"\n"
        "    show(msg)\n"
        "    # --- automatic EDA fallback ---\n"
        "    try:\n"
        "        df_local = globals().get('df')\n"
        "        if df_local is not None:\n"
        "            import pandas as pd\n"
        "            from syntaxmatrix.preface import SB_histplot, _SMX_export_png\n"
        "            num_cols = df_local.select_dtypes(include=['number', 'bool']).columns.tolist()\n"
        "            cat_cols = [c for c in df_local.columns if c not in num_cols]\n"
        "            info = {\n"
        "                'rows': len(df_local),\n"
        "                'cols': len(df_local.columns),\n"
        "                'numeric_cols': len(num_cols),\n"
        "                'categorical_cols': len(cat_cols),\n"
        "            }\n"
        "            show(df_local.head())\n"
        "            show(info)\n"
        "            if num_cols:\n"
        "                SB_histplot()\n"
        "                _SMX_export_png()\n"
        "    except Exception as _f:\n"
        "        show(f\"⚠️ Fallback EDA failed: {type(_f).__name__}: {_f}\")\n"
    )


def harden_ai_code(code: str) -> str:
    """
    Make any AI-generated cell resilient:
      - Safe seaborn wrappers + sentinel vars (boxplot/barplot/etc.)
      - Remove 'numeric_only=' args
      - Replace pd.concat(...) with _safe_concat(...)
      - Relax 'required_cols' hard fails
      - Make static numeric_vars dynamic
      - Wrap the whole block in try/except so no exception bubbles up
    """
    # Remove any LLM-added try/except blocks (hardener adds its own)
    import re

    
    def _strip_stray_backrefs(code: str) -> str:
        code = re.sub(r'(?m)^\s*\\\d+\s*', '', code)     
        code = re.sub(r'(?m)[;]\s*\\\d+\s*', '; ', code)  
        return code
    
    def _patch_feature_coef_dataframe(code: str) -> str:
        """
        Harden patterns like:
            coeffs_df = pd.DataFrame({'feature': num_features, 'coefficient': coef})
        which can crash with:
            ValueError: All arrays must be of the same length
        We wrap them in a try/except and, on failure, rebuild the
        DataFrame by zipping feature names with coefficients up to
        the min length.
        """
        # Match single-line assignments of the form:
        #   <var> = pd.DataFrame({'feature': <feat>, 'coefficient': <coef>})
        import re

        pattern = re.compile(
            r"(?P<indent>^[ \t]*)"
            r"(?P<var>\w+)\s*=\s*pd\.DataFrame\(\s*{\s*"
            r"['\"]feature['\"]\s*:\s*(?P<feat_expr>.+?)\s*,\s*"
            r"['\"]coefficient['\"]\s*:\s*(?P<coef_expr>.+?)\s*"
            r"}\s*\)\s*$",
            re.MULTILINE,
        )

        def repl(m: re.Match) -> str:
            indent = m.group("indent")
            var = m.group("var")
            feat_expr = m.group("feat_expr").strip()
            coef_expr = m.group("coef_expr").strip()

            # Keep the original intent, but add a safe fallback.
            return (
                f"{indent}try:\n"
                f"{indent}    {var} = pd.DataFrame({{'feature': {feat_expr}, 'coefficient': {coef_expr}}})\n"
                f"{indent}except Exception as _e:\n"
                f"{indent}    import numpy as _np\n"
                f"{indent}    _feat = list({feat_expr})\n"
                f"{indent}    _coef = _np.asarray({coef_expr}).ravel()\n"
                f"{indent}    _k = min(len(_feat), len(_coef))\n"
                f"{indent}    {var} = pd.DataFrame({{'feature': _feat[:_k], 'coefficient': _coef[:_k]}})\n"
            )

        return pattern.sub(repl, code)

    def _wrap_metric_calls(code: str) -> str:
        names = [
            "r2_score","accuracy_score","precision_score","recall_score","f1_score",
            "roc_auc_score","classification_report","confusion_matrix",
            "mean_absolute_error","mean_absolute_percentage_error",
            "explained_variance_score","log_loss","average_precision_score",
            "precision_recall_fscore_support"
        ]
        pat = re.compile(r"\b(?:(sklearn\.metrics\.|metrics\.)?(" + "|".join(names) + r"))\s*\(")
        def repl(m):
            prefix = m.group(1) or ""   # "", "metrics.", or "sklearn.metrics."
            name = m.group(2)
            return f"_SMX_call({prefix}{name}, "
        return pat.sub(repl, code)

    def _smx_patch_mean_squared_error_squared_kw():
        """
        sklearn<0.22 doesn't accept mean_squared_error(..., squared=False).
        Patch the module attr so 'from sklearn.metrics import mean_squared_error'
        receives a wrapper that drops 'squared' if the underlying call rejects it.
        """
        try:
            import sklearn.metrics as _sm
            _orig = getattr(_sm, "mean_squared_error", None)
            if not callable(_orig):
                return
            def _mse_compat(y_true, y_pred, *a, **k):
                if "squared" in k:
                    try:
                        return _orig(y_true, y_pred, *a, **k)
                    except TypeError:
                        k.pop("squared", None)
                        return _orig(y_true, y_pred, *a, **k)
                return _orig(y_true, y_pred, *a, **k)
            _sm.mean_squared_error = _mse_compat
        except Exception:
            pass

    def _smx_patch_kmeans_n_init_auto():
        """
        sklearn>=1.4 accepts n_init='auto'; older versions want an int.
        Patch sklearn.cluster.KMeans so 'auto' is converted to 10 if TypeError occurs.
        """
        try:
            import sklearn.cluster as _sc
            _Orig = getattr(_sc, "KMeans", None)
            if _Orig is None:
                return
            class KMeansCompat(_Orig):
                def __init__(self, *a, **k):
                    if isinstance(k.get("n_init", None), str):
                        try:
                            super().__init__(*a, **k)
                            return
                        except TypeError:
                            k["n_init"] = 10
                    super().__init__(*a, **k)
            _sc.KMeans = KMeansCompat
        except Exception:
            pass

    def _smx_patch_ohe_name_api():
        """
        Guard get_feature_names_out on older OneHotEncoder.
        Your templates already use _SMX_OHE; this adds a soft fallback for feature names.
        """
        try:
            from sklearn.preprocessing import OneHotEncoder as _OHE
            _orig_get = getattr(_OHE, "get_feature_names_out", None)
            if _orig_get is None:
                # Monkey-patch instance method via mixin
                def _fallback_get_feature_names_out(self, input_features=None):
                    cats = getattr(self, "categories_", None) or []
                    input_features = input_features or [f"x{i}" for i in range(len(cats))]
                    names = []
                    for base, cat_list in zip(input_features, cats):
                        for j, _ in enumerate(cat_list):
                            names.append(f"{base}__{j}")
                    return names
                _OHE.get_feature_names_out = _fallback_get_feature_names_out
        except Exception:
            pass

    def _ensure_metrics_imports(code: str) -> str:
        needed = set()
        if "r2_score" in code:
            needed.add("r2_score")
        if "mean_absolute_error" in code:
            needed.add("mean_absolute_error")
        # ... add others if you like ...

        if not needed:
            return code

        if "from sklearn.metrics import" in code:
            return code  # assume user/LLM handled it

        import_line = "from sklearn.metrics import " + ", ".join(sorted(needed)) + "\n"
        return import_line + code

    def _fix_unexpected_indent(src: str) -> str:
        """
        Some LLM snippets jump indentation (e.g. extra 8 spaces on an 'import'
        line) without a preceding block opener. That causes
        `IndentationError: unexpected indent` when we wrap in our own `try:`.
        This normalises those lines back to the previous indent level, but only
        when we're not in a multi-line bracket/paren context.
        """
        lines = src.splitlines()
        out = []
        prev_indent = 0
        prev_ends_colon = False
        paren_depth = 0  # (), [], {} depth across lines (very approximate)

        for raw in lines:
            stripped = raw.lstrip()
            if not stripped:  # blank / whitespace line
                out.append(raw)
                continue

            indent = len(raw) - len(stripped)

            # Only flatten if:
            #   - we're not inside a (...) / [...] / {...} block, and
            #   - previous logical line did NOT end with ':', and
            #   - this line is indented more than the previous indent.
            if paren_depth == 0 and not prev_ends_colon and indent > prev_indent:
                indent = prev_indent
            new_line = " " * indent + stripped
            out.append(new_line)

            # Update simple state for next line
            txt = stripped
            paren_depth += txt.count("(") + txt.count("[") + txt.count("{")
            paren_depth -= txt.count(")") + txt.count("]") + txt.count("}")
            prev_ends_colon = txt.rstrip().endswith(":")
            prev_indent = indent

        return "\n".join(out)

    def _fallback_snippet() -> str:
        """
        Final-resort snippet when the LLM code is syntactically broken.

        It:
          - attempts a simple automatic ML task (classification or regression)
          - then falls back to generic but useful EDA.

        It assumes `from syntaxmatrix.preface import *` has already been done,
        so `_SMX_OHE`, `_SMX_call`, `SB_histplot`, `_SMX_export_png` and the
        patched `show()` are available.
        """
        import textwrap

        return textwrap.dedent(
            """\
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            from sklearn.model_selection import train_test_split
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import StandardScaler
            from sklearn.linear_model import LogisticRegression, LinearRegression
            from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error

            df = df.copy()

            # --- basic column introspection ---
            num_cols = df.select_dtypes(include=['number', 'bool']).columns.tolist()
            cat_cols = [c for c in df.columns if c not in num_cols]

            # --- attempt an automatic ML task ---
            target_col = None
            task_type = None

            # Prefer a low-cardinality target (classification)
            for c in num_cols + cat_cols:
                uniq = df[c].dropna().nunique()
                if 2 <= uniq <= 10:
                    target_col = c
                    task_type = 'classification'
                    break

            # If none found, try a numeric regression target
            if target_col is None and num_cols:
                target_col = num_cols[-1]
                task_type = 'regression'

            if target_col is not None:
                try:
                    X = df.drop(columns=[target_col]).copy()
                    y = df[target_col].copy()

                    num_feats = X.select_dtypes(include=['number', 'bool']).columns.tolist()
                    cat_feats = [c for c in X.columns if c not in num_feats]

                    pre = ColumnTransformer(
                        transformers=[
                            ('num', StandardScaler(), num_feats),
                            ('cat', _SMX_OHE(handle_unknown='ignore'), cat_feats),
                        ],
                        remainder='drop',
                    )

                    from sklearn.pipeline import Pipeline
                    if task_type == 'classification':
                        model = LogisticRegression(max_iter=1000)
                    else:
                        model = LinearRegression()

                    pipe = Pipeline([('pre', pre), ('model', model)])

                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.25, random_state=42
                    )

                    pipe.fit(X_train, y_train)
                    y_pred = pipe.predict(X_test)

                    if task_type == 'classification':
                        # If predictions look like probabilities, convert to labels
                        if getattr(y_pred, 'ndim', 1) > 1 and y_pred.shape[1] > 1:
                            y_pred_labels = y_pred.argmax(axis=1)
                        else:
                            try:
                                y_pred_labels = (y_pred > 0.5).astype(y_test.dtype)
                            except Exception:
                                y_pred_labels = y_pred

                        acc = _SMX_call(accuracy_score, y_test, y_pred_labels)
                        show({
                            'target': target_col,
                            'task': 'classification',
                            'accuracy': acc,
                        })
                    else:
                        r2 = _SMX_call(r2_score, y_test, y_pred)
                        mae = _SMX_call(mean_absolute_error, y_test, y_pred)
                        show({
                            'target': target_col,
                            'task': 'regression',
                            'r2': r2,
                            'mae': mae,
                        })

                except Exception as _ml_e:
                    show(f"⚠ ML fallback failed: {type(_ml_e).__name__}: {_ml_e}")

            # --- EDA fallback that still helps answer the question ---
            try:
                info = {
                    'rows': len(df),
                    'cols': len(df.columns),
                    'numeric_cols': len(num_cols),
                    'categorical_cols': len(cat_cols),
                }
                show(df.head(), title='Sample of data')
                show(info, title='Dataset summary')

                # Quick univariate look if we have numeric columns
                if num_cols:
                    SB_histplot()
                    _SMX_export_png()
            except Exception as _eda_e:
                show(f"⚠ EDA fallback failed: {type(_eda_e).__name__}: {_eda_e}")
            """
        )

    def _strip_file_io_ops(code: str) -> str:
        """
        Remove obvious local file I/O operations in LLM code
        so nothing writes to the container filesystem.
        """
        # 1) Methods like df.to_csv(...), df.to_excel(...), etc.
        FILE_WRITE_METHODS = (
            "to_csv", "to_excel", "to_pickle", "to_parquet",
            "to_json", "to_hdf",
        )

        for mname in FILE_WRITE_METHODS:
            pat = re.compile(
                rf"(?m)^(\s*)([A-Za-z_][A-Za-z0-9_\.]*)\s*\.\s*{mname}\s*\([^)]*\)\s*$"
            )

            def _repl(match):
                indent = match.group(1)
                expr = match.group(2)
                return f"{indent}# [SMX] stripped file write: {expr}.{mname}(...)"

            code = pat.sub(_repl, code)

        # 2) plt.savefig(...) calls
        pat_savefig = re.compile(r"(?m)^(\s*)(plt\.savefig\s*\([^)]*\)\s*)$")
        code = pat_savefig.sub(
            lambda m: f"{m.group(1)}# [SMX] stripped savefig: {m.group(2).strip()}",
            code,
        )

        # 3) with open(..., 'w'/'wb') as f:
        pat_with_open = re.compile(
            r"(?m)^(\s*)with\s+open\([^)]*['\"]w[b]?['\"][^)]*\)\s+as\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*$"
        )

        def _with_open_repl(match):
            indent = match.group(1)
            var = match.group(2)
            return f"{indent}if False:  # [SMX] file write stripped (was: with open(... as {var}))"

        code = pat_with_open.sub(_with_open_repl, code)

        # 4) joblib.dump(...), pickle.dump(...)
        for mod in ("joblib", "pickle"):
            pat = re.compile(rf"(?m)^(\s*){mod}\.dump\s*\([^)]*\)\s*$")
            code = pat.sub(
                lambda m: f"{m.group(1)}# [SMX] stripped {mod}.dump(...)",
                code,
            )

        # 5) bare open(..., 'w'/'wb') calls
        pat_open = re.compile(
            r"(?m)^(\s*)open\([^)]*['\"]w[b]?['\"][^)]*\)\s*$"
        )
        code = pat_open.sub(
            lambda m: f"{m.group(1)}# [SMX] stripped open(..., 'w'/'wb')",
            code,
        )

        return code

    # Register and run patches once per execution
    for _patch in (
        _smx_patch_mean_squared_error_squared_kw,
        _smx_patch_kmeans_n_init_auto,
        _smx_patch_ohe_name_api,
    ):
        try:
            _patch()
        except Exception:
            pass

    fixed = code

    fixed = re.sub(
        r"(?s)^\s*try:\s*(.*?)\s*except\s+Exception\s+as\s+\w+:\s*\n\s*show\([^\n]*\)\s*$",
        r"\1",
        fixed.strip()
    )

    # 1) Strip numeric_only=... (version-agnostic)
    fixed = re.sub(r",\s*numeric_only\s*=\s*(True|False|None)", "", fixed, flags=re.I)
    fixed = re.sub(r"\bnumeric_only\s*=\s*(True|False|None)\s*,\s*", "", fixed, flags=re.I)
    fixed = re.sub(r"\bnumeric_only\s*=\s*(True|False|None)\b", "", fixed, flags=re.I)

    # 2) Use safe seaborn wrappers
    fixed = re.sub(r"\bsns\.boxplot\s*\(", "SB_boxplot(", fixed)
    fixed = re.sub(r"\bsns\.barplot\s*\(", "SB_barplot(", fixed)
    fixed = re.sub(r"\bsns\.histplot\s*\(", "SB_histplot(", fixed)
    fixed = re.sub(r"\bsns\.scatterplot\s*\(", "SB_scatterplot(", fixed)

    # 3) Guard concat calls
    fixed = re.sub(r"\bpd\.concat\s*\(", "_safe_concat(", fixed)
    fixed = re.sub(r"\bOneHotEncoder\s*\(", "_SMX_OHE(", fixed)
    # Route np.dot to tolerant matmul
    fixed = re.sub(r"\bnp\.dot\s*\(", "_SMX_mm(", fixed)
    fixed = re.sub(r"(df\s*\[[^\]]+\])\s*\.dt", r"SMX_dt(\1).dt", fixed)


    # 4) Relax any 'required_cols' hard failure blocks
    fixed = re.sub(
        r"required_cols\s*=\s*\[.*?\]\s*?\n\s*missing\s*=\s*\[.*?\]\s*?\n\s*if\s+missing:\s*raise[^\n]+",
        "required_cols = [c for c in df.columns]\n# (relaxed by SMX hardener)",
        fixed,
        flags=re.S,
    )

    # 5) Make static numeric_vars lists dynamic
    fixed = re.sub(
        r"\bnumeric_vars\s*=\s*\[.*?\]",
        "numeric_vars = df.select_dtypes(include=['number','bool']).columns.tolist()",
        fixed,
        flags=re.S,
    )
    # normalise all .dt usages on df[...] / df.attr / df.loc[...] to SMX_dt(...)
    fixed = re.sub(
        r"((?:df\s*(?:\.\s*(?:loc|iloc)\s*)?\[[^\]]+\]|df\s*\.\s*[A-Za-z_]\w*))\s*\.dt\b",
        lambda m: f"SMX_dt({m.group(1)}).dt",
        fixed
    )

    try:
          ast.parse(fixed)
    except (SyntaxError, IndentationError):
        fixed = _fallback_snippet()
        
    fixed = re.sub(
        r"except\s+Exception\s+as\s+e:\s*\n\s*show\(\.\.\.\)",
        "except Exception as e:\n    show(f\"⚠ Block skipped due to: {type(e).__name__}: {e}\")",
        fixed,
    )

    # Fix placeholder Ellipsis handlers from LLM
    fixed = re.sub(
        r"except\s+Exception\s+as\s+e:\s*\n\s*show\(\.\.\.\)",
        "except Exception as e:\n    show(f\"⚠ Block skipped due to: {type(e).__name__}: {e}\")",
        fixed,
    )

    try:
        class _SMXMatmulRewriter(ast.NodeTransformer):
            def visit_BinOp(self, node):
                self.generic_visit(node)
                if isinstance(node.op, ast.MatMult):
                    return ast.Call(func=ast.Name(id="_SMX_mm", ctx=ast.Load()),
                                    args=[node.left, node.right], keywords=[])
                return node
        _tree = ast.parse(fixed)
        _tree = _SMXMatmulRewriter().visit(_tree)
        fixed = ast.unparse(_tree)
    except Exception:
        # If AST rewrite fails, keep original; _SMX_mm will still handle np.dot(...)
        pass

    # 6) Final safety wrapper
    fixed = fixed.replace("\t", "    ")
    fixed = textwrap.dedent(fixed).strip("\n")
    fixed = _ensure_metrics_imports(fixed)
    fixed = _strip_stray_backrefs(fixed)
    fixed = _wrap_metric_calls(fixed)
    fixed = _fix_unexpected_indent(fixed)
    fixed = _patch_feature_coef_dataframe(fixed)
    fixed = _strip_file_io_ops(fixed)

    # Import shared preface helpers once and wrap the LLM body safely
    header = "from syntaxmatrix.preface import *\n\n"
    wrapped = header + wrap_llm_code_safe(fixed)
    return wrapped


def indent_code(code: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line for line in code.splitlines())


def fix_boxplot_placeholder(code: str) -> str:
    # Replace invalid 'sns.boxplot(boxplot)' with a safe call using df/group_label/m
    return re.sub(
        r"sns\.boxplot\(\s*boxplot\s*\)",
        "sns.boxplot(x=group_label, y=m, data=df.loc[df[m].notnull()], showfliers=False)",
        code
    )


def relax_required_columns(code: str) -> str:
    # Remove hard failure on required_cols; keep a soft filter instead
    return re.sub(
        r"required_cols\s*=\s*\[.*?\]\s*?\n\s*missing\s*=\s*\[.*?\]\s*?\n\s*if\s+missing:\s*raise[^\n]+",
        "required_cols = [c for c in df.columns]\n",
        code,
        flags=re.S
    )


def make_numeric_vars_dynamic(code: str) -> str:
    # Replace any static numeric_vars list with a dynamic selection
    return re.sub(
        r"numeric_vars\s*=\s*\[.*?\]",
        "numeric_vars = df.select_dtypes(include=['number','bool']).columns.tolist()",
        code,
        flags=re.S
    )


def auto_inject_template(code: str, intents, df) -> str:
    """If the LLM forgot the core logic, prepend a skeleton block."""

    has_fit = ".fit(" in code
    has_plot = any(k in code for k in ("plt.", "sns.", ".plot(", ".hist("))
    
    UNKNOWN_TOKENS = {
        "unknown","not reported","not_reported","not known","n/a","na",
        "none","nan","missing","unreported","unspecified","null","-",""
    }

    # --- Safe template caller: passes only supported kwargs, falls back cleanly ---
    def _call_template(func, df, **hints):
        import inspect
        try:
            params = inspect.signature(func).parameters
            kw = {k: v for k, v in hints.items() if k in params}
            try:
                return func(df, **kw)
            except TypeError:
                # In case the template changed its signature at runtime
                return func(df)
        except Exception:
            # Absolute safety net
            try:
                return func(df)
            except Exception:
                # As a last resort, return empty code so we don't 500
                return ""

    def _guess_classification_target(df: pd.DataFrame) -> str | None:
        cols = list(df.columns)

        # Helper: does this column look like a sensible label?
        def _is_reasonable_class_col(s: pd.Series, col_name: str) -> bool:
            try:
                nunq = s.dropna().nunique()
            except Exception:
                return False
            # need at least 2 classes, but not hundreds
            if nunq < 2 or nunq > 20:
                return False
            bad_name_keys = ("id", "identifier", "index", "uuid", "key")
            name = str(col_name).lower()
            if any(k in name for k in bad_name_keys):
                return False
            return True

        # 1) columns whose names look like labels
        label_keys = ("target", "label", "outcome", "class", "y", "status")
        name_candidates: list[str] = []
        for key in label_keys:
            for c in cols:
                if key in str(c).lower():
                    name_candidates.append(c)
            if name_candidates:
                break  # keep the earliest matching key-group

        # prioritise name-based candidates that also look like proper label columns
        for c in name_candidates:
            if _is_reasonable_class_col(df[c], c):
                return c
        if name_candidates:
            # fall back to the first name-based candidate if none passed the shape test
            return name_candidates[0]

        # 2) any column with a small number of distinct values (likely a class label)
        for c in cols:
            s = df[c]
            if _is_reasonable_class_col(s, c):
                return c

        # Nothing suitable found
        return None

    def _guess_regression_target(df: pd.DataFrame) -> str | None:
        num_cols = df.select_dtypes(include=[np.number, "bool"]).columns.tolist()
        if not num_cols:
            return None
        # Avoid obvious ID-like columns
        bad_keys = ("id", "identifier", "index")
        candidates = [c for c in num_cols if not any(k in str(c).lower() for k in bad_keys)]
        return (candidates or num_cols)[-1]
    
    def _guess_time_col(df: pd.DataFrame) -> str | None:
        # Prefer actual datetime dtype
        dt_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.datetime64)]
        if dt_cols:
            return dt_cols[0]

        # Fallback: name-based hints
        name_keys = ["date", "time", "timestamp", "datetime", "ds", "period"]
        for c in df.columns:
            name = str(c).lower()
            if any(k in name for k in name_keys):
                return c
        return None

    def _guess_entity_col(df: pd.DataFrame) -> str | None:
        # Typical sequence IDs: id, patient, subject, device, series, entity
        keys = ["id", "patient", "subject", "device", "series", "entity"]
        candidates = []
        for c in df.columns:
            name = str(c).lower()
            if any(k in name for k in keys):
                candidates.append(c)
        return candidates[0] if candidates else None

    def _guess_ts_class_target(df: pd.DataFrame) -> str | None:
        # Try label-like names first
        keys = ["target", "label", "class", "outcome", "y"]
        for key in keys:
            for c in df.columns:
                if key in str(c).lower():
                    return c

        # Fallback: any column with few distinct values (e.g. <= 10)
        for c in df.columns:
            s = df[c]
            # avoid obvious IDs
            if any(k in str(c).lower() for k in ["id", "index"]):
                continue
            try:
                nunq = s.dropna().nunique()
            except Exception:
                continue
            if 1 < nunq <= 10:
                return c

        return None

    def _guess_multilabel_cols(df: pd.DataFrame) -> list[str]:
        cols = list(df.columns)
        lbl_like = [c for c in cols if str(c).startswith(("LBL_", "lbl_"))]
        # also include boolean/binary columns with suitable names
        for c in cols:
            s = df[c]
            try:
                nunq = s.dropna().nunique()
            except Exception:
                continue
            if nunq in (2,) and c not in lbl_like:
                # avoid obvious IDs
                if not any(k in str(c).lower() for k in ("id","index","uuid","identifier")):
                    lbl_like.append(c)
        # keep at most, say, 12 to avoid accidental flood
        return lbl_like[:12]

    def _find_unknownish_column(df: pd.DataFrame) -> str | None:
        # Search categorical-like columns for any 'unknown-like' values or high missingness
        candidates = []
        for c in df.columns:
            s = df[c]
            # focus on object/category/boolean-ish or low-card columns
            if not (pd.api.types.is_object_dtype(s) or pd.api.types.is_categorical_dtype(s) or s.dropna().nunique() <= 20):
                continue
            try:
                vals = s.astype(str).str.strip().str.lower()
            except Exception:
                continue
            # score: presence of unknown tokens + missing rate
            token_hit = int(vals.isin(UNKNOWN_TOKENS).any())
            miss_rate = s.isna().mean()
            name_bonus = int(any(k in str(c).lower() for k in ("status","history","report","known","flag")))
            score = 3*token_hit + 2*name_bonus + miss_rate
            if token_hit or miss_rate > 0.05 or name_bonus:
                candidates.append((score, c))
        if not candidates:
            return None
        candidates.sort(reverse=True)
        return candidates[0][1]

    def _guess_numeric_cols(df: pd.DataFrame, max_n: int = 6) -> list[str]:
        cols = [c for c in df.select_dtypes(include=[np.number, "bool"]).columns if not any(k in str(c).lower() for k in ("id","identifier","index","uuid"))]
        # prefer non-constant columns
        scored = []
        for c in cols:
            try:
                v = df[c].dropna()
                var = float(v.var()) if len(v) else 0.0
                scored.append((var, c))
            except Exception:
                continue
        scored.sort(reverse=True)
        return [c for _, c in scored[:max_n]]

    def _guess_categorical_cols(df: pd.DataFrame, exclude: set[str] | None = None, max_card: int = 12, max_n: int = 5) -> list[str]:
        exclude = exclude or set()
        picks = []
        for c in df.columns:
            if c in exclude:
                continue
            s = df[c]
            if pd.api.types.is_object_dtype(s) or pd.api.types.is_categorical_dtype(s) or s.dropna().nunique() <= max_card:
                nunq = s.dropna().nunique()
                if 2 <= nunq <= max_card and not any(k in str(c).lower() for k in ("id","identifier","index","uuid")):
                    picks.append((nunq, c))
        picks.sort(reverse=True)
        return [c for _, c in picks[:max_n]]

    def _guess_outcome_col(df: pd.DataFrame, exclude: set[str] | None = None) -> str | None:
        exclude = exclude or set()
        # name hints first
        name_keys = ("outcome","target","label","risk","score","result","prevalence","positivity")
        for c in df.columns:
            if c in exclude:
                continue
            name = str(c).lower()
            if any(k in name for k in name_keys) and pd.api.types.is_numeric_dtype(df[c]):
                return c
        # fallback: any binary numeric
        for c in df.select_dtypes(include=[np.number, "bool"]).columns:
            if c in exclude:
                continue
            try:
                if df[c].dropna().nunique() == 2:
                    return c
            except Exception:
                continue
        return None

  
    def _pick_viz_template(signal: str):
        s = signal.lower()

        # explicit chart requests
        if any(k in s for k in ("pie", "donut")):
            return viz_pie

        if any(k in s for k in ("stacked", "100% stacked", "composition", "proportion", "share by")):
            return viz_stacked_bar

        if any(k in s for k in ("distribution", "hist", "histogram", "bins")):
            return viz_distribution

        if any(k in s for k in ("kde", "density")):
            return viz_kde

        # these three you asked about
        if any(k in s for k in ("box", "boxplot", "violin", "spread", "outlier")):
            return viz_box

        if any(k in s for k in ("scatter", "relationship", "vs ", "correlate")):
            return viz_scatter

        if any(k in s for k in ("count", "counts", "frequency", "bar chart", "barplot")):
            return viz_count_bar

        if any(k in s for k in ("area", "trend", "over time", "time series")):
            return viz_area

        # fallback
        return viz_line

    for intent in intents:
        
        if intent not in INJECTABLE_INTENTS:
            return code
    
        # Correlation analysis
        if intent == "correlation_analysis" and not has_fit:
            return eda_correlation(df) + "\n\n" + code

        # Generic visualisation (keyword-based)
        if intent == "visualisation" and not has_fit and not has_plot:
            rq = str(globals().get("refined_question", ""))
            # aq = str(globals().get("askai_question", ""))
            signal = rq + "\n" + str(intents) + "\n" + code
            tpl = _pick_viz_template(signal)
            return tpl(df) + "\n\n" + code
        
        if intent == "clustering" and not has_fit:
            return clustering(df) + "\n\n" + code
                
        if intent == "recommendation" and not has_fit:
            return recommendation(df) + "\\n\\n" + code

        if intent == "topic_modelling" and not has_fit:
            return topic_modelling(df) + "\\n\\n" + code
        
        if intent == "eda" and not has_fit:
            return code + "\n\nSB_heatmap(df.corr())"  # Inject heatmap if 'eda' intent

        # --- Classification ------------------------------------------------
        if intent == "classification" and not has_fit:
            target = _guess_classification_target(df)
            if target:
                return classification(df) + "\n\n" + code
                # return _call_template(classification, df, target) + "\n\n" + code

        # --- Regression ----------------------------------------------------
        if intent == "regression" and not has_fit:
            target = _guess_regression_target(df)
            if target:
                return regression(df) + "\n\n" + code
                # return _call_template(regression, df, target) + "\n\n" + code

        # --- Anomaly detection --------------------------------------------
        if intent == "anomaly_detection":
            uses_anomaly = any(k in code for k in ("IsolationForest", "LocalOutlierFactor", "OneClassSVM"))
            if not uses_anomaly:
                return anomaly_detection(df) + "\n\n" + code

        # --- Time-series anomaly detection --------------------------------
        if intent == "ts_anomaly_detection":
            uses_ts = "STL(" in code or "seasonal_decompose(" in code
            if not uses_ts:
                return ts_anomaly_detection(df) + "\n\n" + code
        
        # --- Time-series classification --------------------------------
        if intent == "time_series_classification" and not has_fit:
            time_col = _guess_time_col(df)
            entity_col = _guess_entity_col(df)
            target_col = _guess_ts_class_target(df)

            # If we can't confidently identify these, do NOT inject anything
            if time_col and entity_col and target_col:
                return time_series_classification(df, entity_col, time_col, target_col) + "\n\n" + code

        # --- Dimensionality reduction --------------------------------------
        if intent == "dimensionality_reduction":
            uses_dr = any(k in code for k in ("PCA(", "TSNE("))
            if not uses_dr:
                return dimensionality_reduction(df) + "\n\n" + code

        # --- Feature selection ---------------------------------------------
        if intent == "feature_selection":
            uses_fs = any(k in code for k in (
                "mutual_info_", "permutation_importance(", "SelectKBest(", "RFE("
            ))
            if not uses_fs:
                return feature_selection(df) + "\n\n" + code

        # --- EDA / correlation / visualisation -----------------------------
        if intent in ("eda", "correlation_analysis", "visualisation") and not has_plot:
            if intent == "correlation_analysis":
                return eda_correlation(df) + "\n\n" + code
            else:
                return eda_overview(df) + "\n\n" + code

        # --- Time-series forecasting ---------------------------------------
        if intent == "time_series_forecasting" and not has_fit:
            uses_ts_forecast = any(k in code for k in (
                "ARIMA", "ExponentialSmoothing", "forecast", "predict("
            ))
            if not uses_ts_forecast:
                return time_series_forecasting(df) + "\n\n" + code
            
        # --- Multi-label classification -----------------------------------
        if intent in ("multilabel_classification",) and not has_fit:
            label_cols = _guess_multilabel_cols(df)
            if len(label_cols) >= 2:
                return multilabel_classification(df, label_cols) + "\n\n" + code

            group_col = _find_unknownish_column(df)
            if group_col:
                num_cols = _guess_numeric_cols(df)
                cat_cols = _guess_categorical_cols(df, exclude={group_col})
                outcome_col = None  # generic; let template skip if not present
                tpl = unknown_group_proxy_pack(df, group_col, UNKNOWN_TOKENS, num_cols, cat_cols, outcome_col)

                # Return template + guarded (repaired) LLM code, so it never crashes
                repaired = make_numeric_vars_dynamic(relax_required_columns(fix_boxplot_placeholder(code)))
                return tpl + "\n\n" + wrap_llm_code_safe(repaired)
                                  
    return code


def fix_values_sum_numeric_only_bug(code: str) -> str:
    """
    If a previous pass injected numeric_only=True into a NumPy-style sum,
    e.g. .values.sum(numeric_only=True), strip it and canonicalize to .to_numpy().sum().
    """
    # .values.sum(numeric_only=True, ...)
    code = re.sub(
        r"\.values\s*\.sum\s*\(\s*[^)]*numeric_only\s*=\s*True[^)]*\)",
        ".to_numpy().sum()",
        code,
        flags=re.IGNORECASE,
    )
    # .to_numpy().sum(numeric_only=True, ...)
    code = re.sub(
        r"\.to_numpy\(\)\s*\.sum\s*\(\s*[^)]*numeric_only\s*=\s*True[^)]*\)",
        ".to_numpy().sum()",
        code,
        flags=re.IGNORECASE,
    )
    return code


def strip_describe_slice(code: str) -> str:
    """
    Remove any pattern like  df.groupby(...).describe()[[ ... ]]  because
    slicing a SeriesGroupBy.describe() causes AttributeError.
    We leave the plain .describe() in place (harmless) and let our own
    table patcher add the correct .agg() table afterwards.
    """
    pat = re.compile(
        r"(df\.groupby\([^)]+\)\[[^\]]+\]\.describe\()\s*\[[^\]]+\]\)",
        flags=re.DOTALL,
    )
    return pat.sub(r"\1)", code)


def remove_plt_show(code: str) -> str:
    """Removes all plt.show() calls from the generated code string."""
    return "\n".join(line for line in code.splitlines() if "plt.show()" not in line)


def patch_plot_with_table(code: str) -> str:
    """
    ▸ strips every `plt.show()` (avoids warnings)
    ▸ converts the *last* Matplotlib / Seaborn figure to PNG-HTML so it is
      rendered in the dashboard
    ▸ appends a summary-stats table **after** the plot
    """
    # 0. drop plt.show()
    lines = [ln for ln in code.splitlines() if "plt.show()" not in ln]

    # 1. locate the last plotting line
    plot_kw = ['plt.', 'sns.', '.plot(', '.boxplot(', '.hist(']
    last_plot = max((i for i,l in enumerate(lines) if any(k in l for k in plot_kw)), default=-1)
    if last_plot == -1:
        return "\n".join(lines)          # nothing to do

    whole = "\n".join(lines)

    # 2. detect group / feature (if any)
    group, feature = None, None
    xm = re.search(r"x\s*=\s*['\"](\w+)['\"]", whole)
    ym = re.search(r"y\s*=\s*['\"](\w+)['\"]", whole)
    if xm and ym:
        group, feature = xm.group(1), ym.group(1)
    else:
        cm = re.search(r"column\s*=\s*['\"](\w+)['\"].*by\s*=\s*['\"](\w+)['\"]", whole)
        if cm:
            feature, group = cm.group(1), cm.group(2)

    # 3. code that captures current fig → PNG → HTML
    img_block = textwrap.dedent("""
        import io, base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode('utf-8')
        from IPython.display import display, HTML
        display(HTML(f'<img src="data:image/png;base64,{img_b64}" style="max-width:100%;">'))          
        plt.close()
    """)

    # 4. build summary-table code
    if group and feature:
        tbl_block = (
            f"summary_table = (\n"
            f"    df.groupby('{group}')['{feature}']\n"
            f"      .agg(['count','mean','std','min','median','max'])\n"
            f"      .rename(columns={{'median':'50%'}})\n"
            f")\n"
        )
    elif ym:
        feature = ym.group(1)
        tbl_block = (
            f"summary_table = (\n"
            f"    df['{feature}']\n"
            f"      .agg(['count','mean','std','min','median','max'])\n"
            f"      .rename(columns={{'median':'50%'}})\n"
            f")\n"
        )
    
    # 3️⃣ grid-search results
    elif "GridSearchCV(" in code:
        tbl_block = textwrap.dedent("""
            # build tidy CV-results table
            cv_df = (
                pd.DataFrame(grid_search.cv_results_)
                .loc[:, ['param_n_estimators', 'param_max_depth',
                        'mean_test_score', 'std_test_score']]
                .rename(columns={
                    'param_n_estimators': 'n_estimators',
                    'param_max_depth':    'max_depth',
                    'mean_test_score':    'mean_cv_accuracy',
                    'std_test_score':     'std'
                })
                .sort_values('mean_cv_accuracy', ascending=False)
                .reset_index(drop=True)
            )
            summary_table = cv_df
        """).strip() + "\n"
    else:
        tbl_block = (
            "summary_table = (\n"
            "    df.describe().T[['count','mean','std','min','50%','max']]\n"
            ")\n"
        )

    tbl_block += "show(summary_table, title='Summary Statistics')"

    # 5. inject image-export block, then table block, after the plot
    patched = (
            lines[:last_plot+1]
            + img_block.splitlines()
            + tbl_block.splitlines()
            + lines[last_plot+1:]
    )
    patched_code = "\n".join(patched)
    # ⬇️ strip every accidental left-indent so top-level lines are flush‐left
    return textwrap.dedent(patched_code)


def refine_eda_question(raw_question, df=None, max_points=1000):
    """
    Rewrites user's EDA question to avoid classic mistakes:
    - For line plots and scatter: recommend aggregation or sampling if large.
    - For histograms/bar: clarify which variable to plot and bin count.
    - For correlation: suggest a heatmap.
    - For counts: direct request for df.shape[0].
    df (optional): pass DataFrame for column inspection.
    """

    # --- SPECIFIC PEARSON CORRELATION DETECTION ----------------------
    pc = re.match(
        r".*\bpearson\b.*\bcorrelation\b.*between\s+(\w+)\s+(and|vs)\s+(\w+)",
        raw_question, re.I
    )
    if pc:
        col1, col2 = pc.group(1), pc.group(3)
        # Return an instruction that preserves the exact intent
        return (
            f"Compute the Pearson correlation coefficient (r) and p-value "
            f"between {col1} and {col2}. "
            f"Print a short interpretation."
        )
    # -----------------------------------------------------------------
    # ── Detect "predict <column>" intent ──────────────────────────────    
    c = re.search(r"\bpredict\s+([A-Za-z0-9_]+)", raw_question, re.I)
    if c:
        target = c.group(1)
        raw_question += (
            f" IMPORTANT: do NOT recreate or overwrite the existing target column "
            f"“{target}”.  Use it as-is for y = df['{target}']."
        )

    q = raw_question.strip()
    # REMOVE explicit summary-table instructions 
    # ── strip any “table” request:  “…table of …”,  “…include table…”,  “…with a table…”
    q = re.sub(r"\b(include|with|and)\b[^.]*\btable[s]?\b[^.]*", "", q, flags=re.I).strip()
    q = re.sub(r"\s*,\s*$", "", q)          # drop trailing comma, if any

    ql = q.lower()

     # ── NEW: if the text contains an exact column name, leave it alone ──
    if df is not None:
        for col in df.columns:
            if col.lower() in ql:
                return q   

    modelling_keywords = (
        "random forest", "gradient-boost", "tree-based model",
        "feature importance", "feature importances",
        "overall accuracy", "train a model", "predict "
    )
    if any(k in ql for k in modelling_keywords):
        return q         

    # 1. Line plots: average if plotting raw numeric vs numeric
    if "line plot" in ql and any(word in ql for word in ["over", "by", "vs"]):
        match = re.search(r'line plot of ([\w_]+) (over|by|vs) ([\w_]+)', ql)
        if match:
            y, _, x = match.groups()
            return f"Show me the average {y} by {x} as a line plot."

    # 2. Scatter plots: sample if too large
    if "scatter" in ql or "scatter plot" in ql:
        if df is not None and df.shape[0] > max_points:
            return q + " (use only a random sample of 1000 points to avoid overplotting)"
        else:
            return q

    # 3. Histogram: specify bins and column
    if "histogram" in ql:
        match = re.search(r'histogram of ([\w_]+)', ql)
        if match:
            col = match.group(1)
            return f"Show me a histogram of {col} using 20 bins."

        # Special case: histogram for column with most missing values
        if "most missing" in ql:
            return (
                "Show a histogram for the column with the most missing values. "
                "First, select the column using: "
                "column_with_most_missing = df.isnull().sum().idxmax(); "
                "then plot its histogram with: "
                "df[column_with_most_missing].hist()"
            )

    # 4. Bar plot: show top N
    if "bar plot" in ql or "bar chart" in ql:
        match = re.search(r'bar (plot|chart) of ([\w_]+)', ql)
        if match:
            col = match.group(2)
            return f"Show me a bar plot of the top 10 {col} values."

    # 5. Correlation or heatmap
    if "correlation" in ql:
        return (
            "Show a correlation heatmap for all numeric columns only. "
            "Use: correlation_matrix = df.select_dtypes(include='number').corr()"
        )


    # 6. Counts/size
    if "how many record" in ql or "row count" in ql or "number of rows" in ql:
        return "How many rows are in the dataset?"

    # 7. General best-practices fallback: add axis labels/titles
    if "plot" in ql:
        return q + " (make sure the axes are labeled and the plot is readable)"
    
    # 8. 
    if (("how often" in ql or "count" in ql or "frequency" in ql) and "category" in ql) or ("value_counts" in q):
        match = re.search(r'(?:categories? in |bar plot of |bar chart of )([\w_]+)', ql)
        col = match.group(1) if match else None
        if col:
            return (
                f"Show a bar plot of the counts of {col} using: "
                f"df['{col}'].value_counts().plot(kind='bar'); "
                "add axis labels and a title, then plt.show()."
            )
    
    if ("mean" in ql and "median" in ql and "standard deviation" in ql) or ("summary statistics" in ql):
        return (
            "Show a table of the mean, median, and standard deviation for all numeric columns. "
            "Use: tbl = df.describe().loc[['mean', '50%', 'std']].rename(index={'50%': 'median'}); display(tbl)"
        )

    # 9. Fallback: return the raw question
    return q


def patch_plot_code(code, df, user_question=None):

     # ── Early guard: abort nicely if the generated code references columns that
    #    do not exist in the DataFrame. This prevents KeyError crashes.
    import re

    
    # ── Detect columns referenced in the code ──────────────────────────
    col_refs = re.findall(r"df\[['\"](\w+)['\"]\]", code)

    # Columns that will be newly CREATED (appear left of '=')
    new_cols = re.findall(r"df\[['\"](\w+)['\"]\]\s*=", code)

    missing_cols = [
        col for col in col_refs
        if col not in df.columns and col not in new_cols
    ]

    if missing_cols:
        cols_list = ", ".join(missing_cols)
        warning = (
            f"show('⚠️ Warning: code references missing column(s): \"{cols_list}\". "
            "These must either exist in df or be created earlier in the code; "
            "otherwise you may see a KeyError.')\n"
        )
        # Prepend the warning but keep the original code so it can still run
        code = warning + code
    
    # 1. For line plots (auto-aggregate)
    m_l = re.search(r"plt\.plot\(\s*df\[['\"](\w+)['\"]\]\s*,\s*df\[['\"](\w+)['\"]\]", code)
    if m_l:
        x, y = m_l.groups()
        if pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y]) and df[x].nunique() > 20:
            return (
                f"agg_df = df.groupby('{x}')['{y}'].mean().reset_index()\n"
                f"plt.plot(agg_df['{x}'], agg_df['{y}'], marker='o')\n"
                f"plt.xlabel('{x}')\nplt.ylabel('{y}')\nplt.title('Average {y} by {x}')\nplt.show()"
            )

    # 2. For scatter plots: sample to 1000 points max
    m_s = re.search(r"plt\.scatter\(\s*df\[['\"](\w+)['\"]\]\s*,\s*df\[['\"](\w+)['\"]\]", code)
    if m_s:
        x, y = m_s.groups()
        if len(df) > 1000:
            return (
                f"samp = df.sample(1000, random_state=42)\n"
                f"plt.scatter(samp['{x}'], samp['{y}'])\n"
                f"plt.xlabel('{x}')\nplt.ylabel('{y}')\nplt.title('{y} vs {x} (sampled)')\nplt.show()"
            )

    # 3. For histograms: use bins=20 for numeric, value_counts for categorical
    m_h = re.search(r"plt\.hist\(\s*df\[['\"](\w+)['\"]\]", code)
    if m_h:
        col = m_h.group(1)
        if pd.api.types.is_numeric_dtype(df[col]):
            return (
                f"plt.hist(df['{col}'], bins=20, edgecolor='black')\n"
                f"plt.xlabel('{col}')\nplt.ylabel('Frequency')\nplt.title('Histogram of {col}')\nplt.show()"
            )
        else:
            # If categorical, show bar plot of value counts
            return (
                f"df['{col}'].value_counts().plot(kind='bar')\n"
                f"plt.xlabel('{col}')\nplt.ylabel('Count')\nplt.title('Counts of {col}')\nplt.show()"
            )

    # 4. For bar plots: show only top 20
    m_b = re.search(r"(?:df\[['\"](\w+)['\"]\]\.value_counts\(\).plot\(kind=['\"]bar['\"]\))", code)
    if m_b:
        col = m_b.group(1)
        if df[col].nunique() > 20:
            return (
                f"topN = df['{col}'].value_counts().head(20)\n"
                f"topN.plot(kind='bar')\n"
                f"plt.xlabel('{col}')\nplt.ylabel('Count')\nplt.title('Top 20 {col} Categories')\nplt.show()"
            )

    # 5. For any DataFrame plot with len(df)>10000, sample before plotting!
    if "df.plot" in code and len(df) > 10000:
        return (
            f"samp = df.sample(1000, random_state=42)\n"
            + code.replace("df.", "samp.")
        )
    
    # ── Block assignment to an existing target column ────────────────        
    #*******************************************************
    target_match = re.search(r"\bpredict\s+([A-Za-z0-9_]+)", user_question or "", re.I)
    if target_match:
        target = target_match.group(1)

        # pattern for an assignment to that target
        assign_pat = rf"df\[['\"]{re.escape(target)}['\"]\]\s*="
        assign_line = re.search(assign_pat + r".*", code)
        if assign_line:
            # runtime check: keep the assignment **only if** the column is absent
            guard = (
                f"if '{target}' in df.columns:\n"
                f"    print('⚠️  {target} already exists – overwrite skipped.');\n"
                f"else:\n"
                f"    {assign_line.group(0)}"
            )
            # remove original assignment line and insert guarded block
            code = code.replace(assign_line.group(0), guard, 1)
    # ***************************************************
    
    # 6. Grouped bar plot for two categoricals
    # Grouped bar plot for two categoricals (.value_counts().unstack() or .groupby().size().unstack())
    if ".value_counts().unstack()" in code or ".groupby(" in code and ".size().unstack()" in code:
        # Try to infer columns from user question if possible:
        group, cat = None, None
        if user_question:
            # crude parse for "counts of X for each Y"
            m = re.search(r"counts? of (\w+) for each (\w+)", user_question)
            if m:
                cat, group = m.groups()
        if not (cat and group):
            # fallback: use two most frequent categoricals
            categoricals = [col for col in df.columns if pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == "object"]
            if len(categoricals) >= 2:
                cat, group = categoricals[:2]
            else:
                # fallback: any
                cat, group = df.columns[:2]
        return (
            f"import pandas as pd\n"
            f"import matplotlib.pyplot as plt\n"
            f"ct = pd.crosstab(df['{group}'], df['{cat}'])\n"
            f"ct.plot(kind='bar')\n"
            f"plt.title('Counts of {cat} for each {group}')\n"
            f"plt.xlabel('{group}')\nplt.ylabel('Count')\nplt.xticks(rotation=0)\nplt.show()"
        )

    # Fallback: Return original code
    return code


def ensure_matplotlib_title(code, title_var="refined_question"):
    import re
    makes_plot = re.search(r"\b(plt\.(plot|scatter|bar|hist)|ax\.(plot|scatter|bar|hist))\b", code)
    has_title = re.search(r"\b(plt\.title|ax\.set_title)\s*\(", code)
    if makes_plot and not has_title:
        code += f"\ntry:\n    plt.title(str({title_var})[:120])\nexcept Exception: pass\n"
    return code


def ensure_output(code: str) -> str:
    """
    Guarantees that AI-generated code actually surfaces results in the UI
    by piping them through syntaxmatrix.display.show().  Works for:
      • bare expressions on the final line
      • chi2/p-value or (stat, p) tuples
      • pd.crosstab results used for χ² tests
    """
    lines = code.rstrip().splitlines()

    # ── 2· capture last bare expression into _out ───────────────────────
    if lines:
        last = lines[-1].strip()
        # not a comment / print / assignment / pyplot call
        if (last and not last.startswith(("print(", "plt.", "#")) and "=" not in last):
            lines[-1] = f"_out = {last}"
            lines.append("show(_out)")

    # ── 3· auto-surface common stats tuples (stat, p) ───────────────────
    # Detect code that assigns something like "chi2, p, dof, expected = ..."    
    if re.search(r"\bchi2\s*,\s*p\s*,", code) and "show((" in code:
        pass   # AI already shows the tuple
    elif re.search(r"\bchi2\s*,\s*p\s*,", code):
        lines.append("show((chi2, p))")

    # ── 4· classification report (string) ───────────────────────────────
    cr_match = re.search(r"^\s*(\w+)\s*=\s*classification_report\(", code, re.M)
    if cr_match and f"show({cr_match.group(1)})" not in "\n".join(lines):
        var = cr_match.group(1)
        lines.append(f"show({var})")
    
    # 5-bis · pivot tables  (DataFrame)
    pivot_match = re.search(r"^\s*(\w+)\s*=\s*.*\.pivot_table\(", code, re.M)
    if pivot_match and f"show({pivot_match.group(1)})" not in "\n".join(lines):
        var = pivot_match.group(1)
        insert_at = next(i for i, l in enumerate(lines) if re.match(rf"\s*{var}\s*=", l)) + 1
        lines.insert(insert_at, "from syntaxmatrix.display import show")
        lines.insert(insert_at + 1, f"show({var})")

    # ── 5· confusion matrix (ndarray → figure) ───────────────────────────
    cm_assign = re.search(r"^\s*(\w+)\s*=\s*confusion_matrix\(", code, re.M)
    if cm_assign and "ConfusionMatrixDisplay" not in code:
        var = cm_assign.group(1)
        lines += [
            "from sklearn.metrics import ConfusionMatrixDisplay",
            "import matplotlib.pyplot as plt",
            "fig = plt.figure(figsize=(4,4))",
            "ax  = fig.gca()",
            f"ConfusionMatrixDisplay(confusion_matrix={var}).plot(ax=ax, colorbar=False)",
            "fig.tight_layout()",
            "plt.show()",
        ]
  
    # ── 6· chi-square contingency tables (pd.crosstab) ──────────────────
    # If a variable named 'crosstab' is created, make sure it's displayed.
    if "crosstab =" in code and "show(crosstab)" not in "\n".join(lines):
        # insert right after the crosstab assignment for readability
        insert_at = next(i for i, l in enumerate(lines) if "crosstab =" in l) + 1
        lines.insert(insert_at, "from syntaxmatrix.display import show")
        lines.insert(insert_at + 1, "show(crosstab)")
    
    # ── 7. AUTO-SHOW scalar counts like  df.shape[0]  or  [...].shape[0]
    assign_scalar = re.match(r"\s*(\w+)\s*=\s*.+\.shape\[\s*0\s*\]\s*$", lines[-1])
    if assign_scalar:
        var = assign_scalar.group(1)
        lines.append(f"show({var})") 

    # ── 8. utils.ensure_output()
    assign_df = re.match(r"\s*(\w+)\s*=\s*df\[", lines[-1])
    if assign_df:
        var = assign_df.group(1)
        lines.append(f"show({var})")
        
    return "\n".join(lines)


def get_plotting_imports(code):
    imports = []
    if "plt." in code and "import matplotlib.pyplot as plt" not in code:
        imports.append("import matplotlib.pyplot as plt")
    if "sns." in code and "import seaborn as sns" not in code:
        imports.append("import seaborn as sns")
    if "px." in code and "import plotly.express as px" not in code:
        imports.append("import plotly.express as px")
    if "pd." in code and "import pandas as pd" not in code:
        imports.append("import pandas as pd")
    if "np." in code and "import numpy as np" not in code:
        imports.append("import numpy as np")
    if "display(" in code and "from IPython.display import display" not in code:
        imports.append("from IPython.display import display")
    # Optionally, add more as you see usage (e.g., import scipy, statsmodels, etc)
    if imports:
        code = "\n".join(imports) + "\n\n" + code
    return code


def patch_pairplot(code, df):
    if "sns.pairplot" in code:
        # Always assign and print pairgrid
        code = re.sub(r"sns\.pairplot\((.+)\)", r"pairgrid = sns.pairplot(\1)", code)
        if "plt.show()" not in code:
            code += "\nplt.show()"
        if "print(pairgrid)" not in code:
            code += "\nprint(pairgrid)"
    return code


def ensure_image_output(code: str) -> str:
    """
    Replace each plt.show() with an indented _SMX_export_png() call.
    This keeps block indentation valid and still renders images in the dashboard.
    """
    if "plt.show()" not in code:
        return code

    import re
    out_lines = []
    for ln in code.splitlines():
        if "plt.show()" not in ln:
            out_lines.append(ln)
            continue

        # works for:
        #   plt.show()
        #   plt.tight_layout(); plt.show()
        #   ... ; plt.show(); ...  (multiple on one line)
        indent = re.match(r"^(\s*)", ln).group(1)
        parts = ln.split("plt.show()")

        # keep whatever is before the first plt.show()
        if parts[0].strip():
            out_lines.append(parts[0].rstrip())

        # for every plt.show() we removed, insert exporter at same indent
        for _ in range(len(parts) - 1):
            out_lines.append(indent + "_SMX_export_png()")

        # keep whatever comes after the last plt.show()
        if parts[-1].strip():
            out_lines.append(indent + parts[-1].lstrip())

    return "\n".join(out_lines)


def clean_llm_code(code: str) -> str:
    """
    Make LLM output safe to exec:
    - If fenced blocks exist, keep the largest one (usually the real code).
    - Otherwise strip any stray ``` / ```python lines.
    - Remove common markdown/preamble junk.
    """
    code = str(code or "")

    # Extract fenced blocks (```python ... ``` or ``` ... ```)
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", code, flags=re.I | re.S)

    if blocks:
        # pick the largest block; small trailing blocks are usually garbage
        largest = max(blocks, key=lambda b: len(b.strip()))
        if len(largest.strip().splitlines()) >= 10:
            code = largest
        else:
            # if no meaningful block, just remove fence markers
            code = re.sub(r"^```.*?$", "", code, flags=re.M)
    else:
        # no complete blocks — still remove any stray fence lines
        code = re.sub(r"^```.*?$", "", code, flags=re.M)

    # Strip common markdown/preamble lines
    drop_prefixes = (
        "here is", "here's", "below is", "sure,", "certainly",
        "explanation", "note:", "```"
    )
    cleaned_lines = []
    for ln in code.splitlines():
        s = ln.strip().lower()
        if any(s.startswith(p) for p in drop_prefixes):
            continue
        cleaned_lines.append(ln)

    return "\n".join(cleaned_lines).strip()


def fix_groupby_describe_slice(code: str) -> str:
    """
    Replaces  df.groupby(...).describe()[[...] ]  with a safe .agg(...)
    so it works for both SeriesGroupBy and DataFrameGroupBy.
    """
    pat = re.compile(
        r"(df\.groupby\(['\"][\w]+['\"]\)\['[\w]+['\"]\]\.describe\()\s*\[\[([^\]]+)\]\]\)", 
        re.MULTILINE
    )
    def repl(match):
        inner = match.group(0)
        # extract group and feature to build df.groupby('g')['f']
        g = re.search(r"groupby\('([\w]+)'\)", inner).group(1)
        f = re.search(r"\)\['([\w]+)'\]\.describe", inner).group(1)
        return (
            f"df.groupby('{g}')['{f}']"
            ".agg(['count','mean','std','min','median','max'])"
            ".rename(columns={'median':'50%'})"
        )
    return pat.sub(repl, code)


def fix_importance_groupby(code: str) -> str:
    pattern = re.compile(r"df\.groupby\(['\"]Importance['\"]\)\['\"?Importance['\"]?\]")
    if "importance_df" in code:
        return pattern.sub("importance_df.groupby('Importance')['Importance']", code)
    return code

def inject_auto_preprocessing(code: str) -> str:
    """
    • Detects a RandomForestClassifier in the generated code.
    • Finds the target column from `y = df['target']`.
    • Prepends a fully-dedented preprocessing snippet that:
        – auto-detects numeric & categorical columns
        – builds a ColumnTransformer (OneHotEncoder + StandardScaler)
    The dedent() call guarantees no leading-space IndentationError.
    """
    if "RandomForestClassifier" not in code:
        return code                      # nothing to patch

    y_match = re.search(r"y\s*=\s*df\[['\"]([^'\"]+)['\"]\]", code)
    if not y_match:
        return code                      # can't infer target safely
    target = y_match.group(1)

    prep_snippet = textwrap.dedent(f"""
        # ── automatic preprocessing ───────────────────────────────
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        num_cols = [c for c in num_cols if c != '{target}']
        cat_cols = [c for c in cat_cols if c != '{target}']

        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder

        preproc = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
            ],
            remainder='drop',
        )
        # ───────────────────────────────────────────────────────────
    """).strip() + "\n\n"

    # simply prepend; model code that follows can wrap estimator in a Pipeline
    return prep_snippet + code


def fix_to_datetime_errors(code: str) -> str:
    """
    Force every pd.to_datetime(…) call to ignore bad dates so that
    
    'year 16500 is out of range' and similar issues don’t crash runs.
    """
    import re
    # look for any pd.to_datetime( … )
    pat = re.compile(r"pd\.to_datetime\(([^)]+)\)")
    def repl(m):
        inside = m.group(1)
        # if the call already has errors=, leave it unchanged
        if "errors=" in inside:
            return m.group(0)
        return f"pd.to_datetime({inside}, errors='coerce')"
    return pat.sub(repl, code)


def fix_numeric_sum(code: str) -> str:
    """
    Make .sum(...) code safe across pandas versions by removing any
    numeric_only=... argument (True/False/None) from function calls.

    This avoids errors on pandas versions where numeric_only is not
    supported for Series/grouped sums, and we rely instead on explicit
    numeric column selection (e.g. select_dtypes) in the generated code.
    """
    # Case 1: ..., numeric_only=True/False/None
    code = re.sub(
        r",\s*numeric_only\s*=\s*(True|False|None)",
        "",
        code,
        flags=re.IGNORECASE,
    )

    # Case 2: numeric_only=True/False/None, ...  (as first argument)
    code = re.sub(
        r"numeric_only\s*=\s*(True|False|None)\s*,\s*",
        "",
        code,
        flags=re.IGNORECASE,
    )

    # Case 3: numeric_only=True/False/None  (only argument)
    code = re.sub(
        r"numeric_only\s*=\s*(True|False|None)",
        "",
        code,
        flags=re.IGNORECASE,
    )

    return code


def fix_concat_empty_list(code: str) -> str:
    """
    Make pd.concat calls resilient to empty lists of objects.

    Transforms patterns like:
        pd.concat(frames, ignore_index=True)
        pd.concat(frames)

    into:
        pd.concat(frames or [pd.DataFrame()], ignore_index=True)
        pd.concat(frames or [pd.DataFrame()])

    Only triggers when the first argument is a simple variable name.
    """
    pattern = re.compile(r"pd\.concat\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*(,|\))")

    def _repl(m):
        name = m.group(1)
        sep = m.group(2)  # ',' or ')'
        return f"pd.concat({name} or [pd.DataFrame()]{sep}"

    return pattern.sub(_repl, code)


def fix_numeric_aggs(code: str) -> str:
    _AGG_FUNCS = ("sum", "mean") 
    pat = re.compile(rf"\.({'|'.join(_AGG_FUNCS)})\(\s*([^)]+)?\)")
    def _repl(m):
        func, args = m.group(1), m.group(2) or ""
        if "numeric_only" in args:
            return m.group(0)
        args = args.rstrip()
        if args:
            args += ", "
        return f".{func}({args}numeric_only=True)"
    return pat.sub(_repl, code)


def ensure_accuracy_block(code: str) -> str:
    """
    Inject a sensible evaluation block right after the last `<est>.fit(...)`
    Classification → accuracy + weighted F1
    Regression    → R², RMSE, MAE
    Heuristic: infer task from estimator names present in the code.
    """
    import re, textwrap

    # If any proper metric already exists, do nothing
    if re.search(r"\b(accuracy_score|f1_score|r2_score|mean_squared_error|mean_absolute_error)\b", code):
        return code

    # Find the last "<var>.fit(" occurrence to reuse the estimator variable name
    m = list(re.finditer(r"(\w+)\.fit\s*\(", code))
    if not m:
        return code  # no estimator

    var = m[-1].group(1)
    # indent with same leading whitespace used on that line
    indent = re.match(r"\s*", code[m[-1].start():]).group(0)

    # Detect regression by estimator names / hints in code
    is_regression = bool(
        re.search(
            r"\b(LinearRegression|Ridge|Lasso|ElasticNet|ElasticNetCV|HuberRegressor|TheilSenRegressor|RANSACRegressor|"
            r"RandomForestRegressor|GradientBoostingRegressor|DecisionTreeRegressor|KNeighborsRegressor|SVR|"
            r"XGBRegressor|LGBMRegressor|CatBoostRegressor)\b", code
        )
        or re.search(r"\bOLS\s*\(", code)
        or re.search(r"\bRegressor\b", code)
    )

    if is_regression:
        # inject numpy import if needed for RMSE
        if "import numpy as np" not in code and "np." not in code:
            code = "import numpy as np\n" + code
        eval_block = textwrap.dedent(f"""
            {indent}# ── automatic regression evaluation ─────────
            {indent}from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
            {indent}y_pred = {var}.predict(X_test)
            {indent}r2 = r2_score(y_test, y_pred)
            {indent}rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
            {indent}mae = float(mean_absolute_error(y_test, y_pred))
            {indent}print(f"R²: {{r2:.4f}} | RMSE: {{rmse:.4f}} | MAE: {{mae:.4f}}")
        """)
    else:
        eval_block = textwrap.dedent(f"""
            {indent}# ── automatic classification evaluation ─────────
            {indent}from sklearn.metrics import accuracy_score, f1_score
            {indent}y_pred = {var}.predict(X_test)
            {indent}acc = accuracy_score(y_test, y_pred)
            {indent}f1  = f1_score(y_test, y_pred, average='weighted')
            {indent}print(f"Accuracy: {{acc:.2%}} | F1 (weighted): {{f1:.3f}}")
        """)

    insert_at = code.find("\n", m[-1].end()) + 1
    return code[:insert_at] + eval_block + code[insert_at:]


def fix_scatter_and_summary(code: str) -> str:
    """
    1. Change  cmap='spectral'  (any case) → cmap='Spectral'
    2. If the LLM forgets to close the parenthesis in
         summary_table = ( df.describe()...   <missing )>
       insert the ')' right before the next 'from' or 'show('.
    """
    # 1️⃣ colormap case
    code = re.sub(
        r"cmap\s*=\s*['\"]spectral['\"]",          # insensitive pattern
        "cmap='Spectral'",
        code,
        flags=re.IGNORECASE,
    )

    # 2️⃣ close summary_table = ( ... )
    code = re.sub(
        r"(summary_table\s*=\s*\(\s*df\.describe\([^\n]+?\n)"
        r"(?=\s*(from|show\())",                  # look-ahead: next line starts with 'from' or 'show('
        r"\1)",                                   # keep group 1 and add ')'
        code,
        flags=re.MULTILINE,
    )

    return code


def auto_format_with_black(code: str) -> str:
    """
    Format the generated code with Black. Falls back silently if Black
    is missing or raises (so the dashboard never 500s).
    """
    try:
        import black  # make sure black is in your v-env:  pip install black

        mode = black.FileMode()          # default settings
        return black.format_str(code, mode=mode)

    except Exception:
        return code        


def ensure_preproc_in_pipeline(code: str) -> str:
    """
    If code defines `preproc = ColumnTransformer(...)` but then builds
    `Pipeline([('scaler', StandardScaler()), ('clf', ...)])`, replace
    that stanza with `Pipeline([('prep', preproc), ('clf', ...)])`.
    """
    return re.sub(
        r"Pipeline\(\s*\[\('scaler',\s*StandardScaler\(\)\)",
        "Pipeline([('prep', preproc)",
        code
    )


def fix_plain_prints(code: str) -> str:
    """
    Rewrite bare `print(var)` where var looks like a dataframe/series/ndarray/etc
    to go through SyntaxMatrix's smart display (so it renders in the dashboard).
    Keeps string prints alone.
    """

    # Skip obvious string-literal prints
    new = re.sub(
        r"(?m)^\s*print\(\s*([A-Za-z_]\w*)\s*\)\s*$",
        r"from syntaxmatrix.display import show\nshow(\1)",
        code,
    )
    return new


def fix_print_html(code: str) -> str:
    """
    Ensure that HTML / DataFrame HTML are *displayed* (and captured by the kernel),
    not printed as `<IPython.core.display.HTML object>` to the server console.
    - Rewrites: print(HTML(...))  → display(HTML(...))
                print(display(...)) → display(...)
                print(df.to_html(...)) → display(HTML(df.to_html(...)))
    Also prepends `from IPython.display import display, HTML` if required.
    """
    import re

    new = code

    # 1) print(HTML(...)) -> display(HTML(...))
    new = re.sub(r"(?m)^\s*print\s*\(\s*HTML\s*\(", "display(HTML(", new)

    # 2) print(display(...)) -> display(...)
    new = re.sub(r"(?m)^\s*print\s*\(\s*display\s*\(", "display(", new)

    # 3) print(<expr>.to_html(...)) -> display(HTML(<expr>.to_html(...)))
    new = re.sub(
        r"(?m)^\s*print\s*\(\s*([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*\.to_html\s*\(",
        r"display(HTML(\1.to_html(", new
    )

    # If code references HTML() or display() make sure the import exists
    if ("HTML(" in new or re.search(r"\bdisplay\s*\(", new)) and \
        "from IPython.display import display, HTML" not in new:
        new = "from IPython.display import display, HTML\n" + new

    return new


def ensure_ipy_display(code: str) -> str:
    """
    Guarantee that the cell has proper IPython display imports so that
    display(HTML(...)) produces 'display_data' events the kernel captures.
    """
    if "display(" in code and "from IPython.display import display, HTML" not in code:
        return "from IPython.display import display, HTML\n" + code
    return code


def drop_bad_classification_metrics(code: str, y_or_df) -> str:
    """
    Remove classification metrics (accuracy_score, classification_report, confusion_matrix)
    if the generated cell is *regression*. We infer this from:
      1) The estimator names in the code (LinearRegression, OLS, Regressor*, etc.), OR
      2) The target dtype if we can parse y = df['...'] and have the DataFrame.
    Safe across datasets and queries.
    """
    import re
    import pandas as pd

    # 1) Heuristic by estimator names in the *code* (fast path)
    regression_by_model = bool(re.search(
        r"\b(LinearRegression|Ridge|Lasso|ElasticNet|ElasticNetCV|HuberRegressor|TheilSenRegressor|RANSACRegressor|"
        r"RandomForestRegressor|GradientBoostingRegressor|DecisionTreeRegressor|KNeighborsRegressor|SVR|"
        r"XGBRegressor|LGBMRegressor|CatBoostRegressor)\b", code
    ) or re.search(r"\bOLS\s*\(", code))

    is_regression = regression_by_model

    # 2) If not obvious from the model, try to infer from y dtype (if we can)
    if not is_regression:
        try:
            # Try to parse: y = df['target']
            m = re.search(r"y\s*=\s*df\[['\"]([^'\"]+)['\"]\]", code)
            if m and hasattr(y_or_df, "columns") and m.group(1) in getattr(y_or_df, "columns", []):
                y = y_or_df[m.group(1)]
                if pd.api.types.is_numeric_dtype(y) and y.nunique(dropna=True) > 10:
                    is_regression = True
            else:
                # If a Series was passed
                y = y_or_df
                if hasattr(y, "dtype") and pd.api.types.is_numeric_dtype(y) and y.nunique(dropna=True) > 10:
                    is_regression = True
        except Exception:
            pass

    if is_regression:
        # Strip classification-only lines
        for pat in (r"\n.*accuracy_score[^\n]*", r"\n.*classification_report[^\n]*", r"\n.*confusion_matrix[^\n]*"):
            code = re.sub(pat, "", code, flags=re.I)

    return code


def force_capture_display(code: str) -> str:
    """
    Ensure our executor captures HTML output:
    - Remove any import that would override our 'display' hook.
    - Keep/allow importing HTML only.
    - Handle alias cases like 'display as d'.
    """
    import re
    new = code

    # 'from IPython.display import display, HTML' -> keep HTML only
    new = re.sub(
        r"(?m)^\s*from\s+IPython\.display\s+import\s+display\s*,\s*HTML\s*(?:as\s+([A-Za-z_]\w*))?\s*$",
        r"from IPython.display import HTML\1", new
    )

    # 'from IPython.display import display as d' -> 'd = display'
    new = re.sub(
        r"(?m)^\s*from\s+IPython\.display\s+import\s+display\s+as\s+([A-Za-z_]\w+)\s*$",
        r"\1 = display", new
    )

    # 'from IPython.display import display' -> remove (use our injected display)
    new = re.sub(
        r"(?m)^\s*from\s+IPython\.display\s+import\s+display\s*$",
        r"# display import removed (SMX capture active)", new
    )

    # If someone does 'import IPython.display as disp' and calls disp.display(...), rewrite to display(...)
    new = re.sub(
        r"(?m)\bIPython\.display\.display\s*\(",
        "display(", new
    )
    new = re.sub(
        r"(?m)\b([A-Za-z_]\w*)\.display\s*\("  # handles 'disp.display(' after 'import IPython.display as disp'
        r"(?=.*import\s+IPython\.display\s+as\s+\1)",
        "display(", new
    )
    return new


def strip_matplotlib_show(code: str) -> str:
    """Remove blocking plt.show() calls (we export base64 instead)."""
    import re
    return re.sub(r"(?m)^\s*plt\.show\(\)\s*$", "", code)


def inject_display_shim(code: str) -> str:
    """
    Provide display()/HTML() if missing, forwarding to our executor hook.
    Harmless if the names already exist.
    """
    shim = (
        "try:\n"
        "    display\n"
        "except NameError:\n"
        "    def display(obj=None, **kwargs):\n"
        "        __builtins__.get('_smx_display', print)(obj)\n"
        "try:\n"
        "    HTML\n"
        "except NameError:\n"
        "    class HTML:\n"
        "        def __init__(self, data): self.data = str(data)\n"
        "        def _repr_html_(self): return self.data\n"
        "\n"
    )
    return shim + code


def strip_spurious_column_tokens(code: str) -> str:
    """
    Remove common stop-words ('the','whether', ...) when they appear
    inside column lists, e.g.:
        predictors = ['BMI','the','HbA1c']
        df[['GGT','whether','BMI']]
    Leaves other strings intact.
    """
    STOP = {
        "the","whether","a","an","and","or","of","to","in","on","for","by",
        "with","as","at","from","that","this","these","those","is","are","was","were", 
        "coef", "Coef", "coefficient", "Coefficient"
    }

    def _norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", s.lower())

    def _clean_list(content: str) -> str:
        # Rebuild a string list, keeping only non-stopword items
        items = re.findall(r"(['\"])(.*?)\1", content)
        if not items:
            return "[" + content + "]"
        keep = [f"{q}{s}{q}" for (q, s) in items if _norm(s) not in STOP]
        return "[" + ", ".join(keep) + "]"

    # Variable assignments: predictors/features/columns/cols = [...]
    code = re.sub(
        r"(?m)\b(predictors|features|columns|cols)\s*=\s*\[([^\]]+)\]",
        lambda m: f"{m.group(1)} = " + _clean_list(m.group(2)),
        code
    )

    # df[[ ... ]] selections
    code = re.sub(
        r"df\s*\[\s*\[([^\]]+)\]\s*\]", lambda m: "df[" + _clean_list(m.group(1)) + "]", code)

    return code


def patch_prefix_seaborn_calls(code: str) -> str:
    """
    Ensure bare seaborn calls are prefixed with `sns.`.
    E.g., `barplot(...)` → `sns.barplot(...)`, `heatmap(...)` → `sns.heatmap(...)`, etc.
    """
    if "sns." in code:
        # still fix any leftover bare calls alongside prefixed ones
        pass

    # functions commonly used from seaborn
    funcs = [
        "barplot","countplot","boxplot","violinplot","stripplot","swarmplot",
        "histplot","kdeplot","jointplot","pairplot","heatmap","clustermap",
        "scatterplot","lineplot","catplot","displot","lmplot"
    ]
    # Replace bare function calls not already qualified by a dot (e.g., obj.barplot)
    # (?<![\w.]) ensures no preceding word char or dot; avoids touching obj.barplot or mybarplot
    pattern = re.compile(r"(?<![\w\.])(" + "|".join(funcs) + r")\s*\(", flags=re.MULTILINE)

    def _add_prefix(m):
        fn = m.group(1)
        return f"sns.{fn}("

    return pattern.sub(_add_prefix, code)


def patch_ensure_seaborn_import(code: str) -> str:
    """
    If seaborn is used (sns.) ensure `import seaborn as sns` exists once.
    Also set a quiet theme for consistent visuals.
    """
    needs_sns = "sns." in code
    has_import = bool(re.search(r"^\s*import\s+seaborn\s+as\s+sns\s*$", code, flags=re.MULTILINE))
    if needs_sns and not has_import:
        # Insert after the first block of imports if possible, else at top
        import_block = re.search(r"^(?:\s*(?:from\s+\S+\s+import\s+.+|import\s+\S+)\s*\n)+", code, flags=re.MULTILINE)
        inject = "import seaborn as sns\ntry:\n    sns.set_theme()\nexcept Exception:\n    pass\n"
        if import_block:
            start = import_block.end()
            code = code[:start] + inject + code[start:]
        else:
            code = inject + code
    return code


def patch_pie_chart(code, df, user_question=None, top_n: int = 12):
    """
    Normalise pie-chart requests.

    Supports three patterns:
    A) Threshold split cohorts, e.g. "HbA1c ≥ 6.5 vs < 6.5" → two pies per categorical + grouped bar.
    B) Facet-by categories, e.g. "Ethnicity across BMI categories" or "bin BMI into Normal/Overweight/Obese"
       → one pie per facet level (grid) + counts bar of facet sizes.
    C) Single pie when no split/facet is requested.

    Notes:
    - Pie variables must be categorical (or numeric binned).
    - Facet variables can be categorical or numeric (we bin numeric; BMI gets WHO bins).
    """

    q = (user_question or "")
    q_low = q.lower()

    # Prefer explicit: df['col'].value_counts()
    m = re.search(r"df\[['\"](\w+)['\"]\]\.value_counts\(", code)
    col = m.group(1) if m else None

    # ---------- helpers ----------
    def _is_cat(col):
        return (str(df[col].dtype).startswith("category")
                or df[col].dtype == "object"
                or (pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() <= 20))

    def _cats_from_question(question: str):
        found = []
        for c in df.columns:
            if c.lower() in question.lower() and _is_cat(c):
                found.append(c)
        # dedupe preserve order
        seen, out = set(), []
        for c in found:
            if c not in seen:
                out.append(c); seen.add(c)
        return out

    def _fallback_cat():
        cats = [(c, df[c].nunique()) for c in df.columns if _is_cat(c) and df[c].nunique() > 1]
        if not cats: return None
        cats.sort(key=lambda t: t[1])
        return cats[0][0]
    
    def _infer_comp_pref(question: str) -> str:
        ql = (question or "").lower()
        if "heatmap" in ql or "matrix" in ql:
            return "heatmap"
        if "100%" in ql or "100 percent" in ql or "proportion" in ql or "share" in ql or "composition" in ql:
            return "stacked_bar_pct"
        if "stacked" in ql:
            return "stacked_bar"
        if "grouped" in ql or "clustered" in ql or "side-by-side" in ql:
            return "grouped_bar"
        return "counts_bar"

    # parse threshold split like "HbA1c ≥ 6.5"
    def _parse_split(question: str):
        ops_map = {"≥": ">=", "≤": "<=", ">=": ">=", "<=": "<=", ">": ">", "<": "<", "==": "==", "=": "=="}
        m = re.search(r"([A-Za-z_][A-Za-z0-9_ ]*)\s*(≥|<=|≤|>=|>|<|==|=)\s*([0-9]+(?:\.[0-9]+)?)", question)
        if not m: return None
        col_raw, op_raw, val_raw = m.group(1).strip(), m.group(2), m.group(3)
        op = ops_map.get(op_raw); 
        if not op: return None
        # case-insensitive column match
        candidates = {c.lower(): c for c in df.columns}
        col = candidates.get(col_raw.lower())
        if not col: return None
        try: val = float(val_raw)
        except Exception: return None
        return (col, op, val)

    # facet extractor: "by/ across / within each / per <col>", or "bin <col>", or named category list
    def _extract_facet(question: str):
        # 1) explicit "by/ across / within / per <col>"
        for kw in [" by ", " across ", " within ", " within each ", " per "]:
            m = re.search(kw + r"([A-Za-z_][A-Za-z0-9_ ]*)", " " + question + " ", flags=re.IGNORECASE)
            if m:
                col_raw = m.group(1).strip()
                candidates = {c.lower(): c for c in df.columns}
                if col_raw.lower() in candidates:
                    return (candidates[col_raw.lower()], "auto")
        # 2) "bin <col>"
        m2 = re.search(r"bin\s+([A-Za-z_][A-Za-z0-9_ ]*)", question, flags=re.IGNORECASE)
        if m2:
            col_raw = m2.group(1).strip()
            candidates = {c.lower(): c for c in df.columns}
            if col_raw.lower() in candidates:
                return (candidates[col_raw.lower()], "bin")
        # 3) BMI special: mentions of normal/overweight/obese imply BMI categories
        if any(kw in question.lower() for kw in ["normal", "overweight", "obese", "obesity"]) and \
           any(c.lower() == "bmi" for c in df.columns.str.lower()):
            bmi_col = [c for c in df.columns if c.lower() == "bmi"][0]
            return (bmi_col, "bmi")
        return None

    def _bmi_bins(series: pd.Series):
        # WHO cutoffs
        bins   = [-np.inf, 18.5, 25, 30, np.inf]
        labels = ["Underweight (<18.5)", "Normal (18.5–24.9)", "Overweight (25–29.9)", "Obese (≥30)"]
        return pd.cut(series.astype(float), bins=bins, labels=labels, right=False)

    wants_pie = ("pie" in q_low) or ("plt.pie(" in code) or ("kind='pie'" in code) or ('kind="pie"' in code)
    if not wants_pie:
        return code

    split = _parse_split(q)              
    facet = _extract_facet(q)             
    cats = _cats_from_question(q)       
    _comp_pref = _infer_comp_pref(q)

    # Prefer explicitly referenced categorical like Ethnicity, Smoking_Status, Physical_Activity_Level
    for hard in ["Ethnicity", "Smoking_Status", "Physical_Activity_Level"]:
        if hard in df.columns and hard not in cats and hard.lower() in q_low:
            cats.append(hard)

    # --------------- CASE A: threshold split (cohorts) ---------------
    if split:
        if not (cats or any(_is_cat(c) for c in df.columns)):
            return code
        if not cats:
            pool = [(c, df[c].nunique()) for c in df.columns if _is_cat(c) and df[c].nunique() > 1]
            pool.sort(key=lambda t: t[1])
            cats = [t[0] for t in pool[:3]] if pool else []
        if not cats:
            return code

        split_col, op, val = split
        cond_str = f"(df['{split_col}'] {op} {val})"
        snippet = f"""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        _mask_a = ({cond_str}) & df['{split_col}'].notna()
        _mask_b = (~({cond_str})) & df['{split_col}'].notna()

        _cohort_a_name = "{split_col} {op} {val}"
        _cohort_b_name = "NOT ({split_col} {op} {val})"

        _cat_cols = {cats!r}
        n = len(_cat_cols)
        fig, axes = plt.subplots(nrows=n, ncols=2, figsize=(12, 5*n))
        if n == 1:
            axes = np.array([axes])

        for i, col in enumerate(_cat_cols):
            s_a = df.loc[_mask_a, col].astype(str).value_counts().nlargest({top_n})
            s_b = df.loc[_mask_b, col].astype(str).value_counts().nlargest({top_n})

            ax_a = axes[i, 0]; ax_b = axes[i, 1]
            if len(s_a) > 0:
                ax_a.pie(s_a.values, labels=[str(x) for x in s_a.index],
                        autopct='%1.1f%%', startangle=90, counterclock=False)
            ax_a.set_title(f"{{col}} — {{_cohort_a_name}}"); ax_a.axis('equal')

            if len(s_b) > 0:
                ax_b.pie(s_b.values, labels=[str(x) for x in s_b.index],
                        autopct='%1.1f%%', startangle=90, counterclock=False)
            ax_b.set_title(f"{{col}} — {{_cohort_b_name}}"); ax_b.axis('equal')

        plt.tight_layout(); plt.show()

        # grouped bar complement
        for col in _cat_cols:
            _tmp = (df.loc[df['{split_col}'].notna(), [col, '{split_col}']]
              .assign(__cohort=np.where({cond_str}, _cohort_a_name, _cohort_b_name)))
            _tab = _tmp.groupby([col, "__cohort"]).size().unstack("__cohort").fillna(0)
            _tab = _tab.loc[_tab.sum(axis=1).sort_values(ascending=False).index[:{top_n}]]

            if _comp_pref == "grouped_bar":
                ax = _tab.plot(kind='bar', rot=0, figsize=(10, 4))
                ax.set_title(f"{col} by cohort (grouped)")
                ax.set_xlabel(col); ax.set_ylabel("Count")
                plt.tight_layout(); plt.show()

            elif _comp_pref == "stacked_bar":
                ax = _tab.plot(kind='bar', stacked=True, rot=0, figsize=(10, 4))
                ax.set_title(f"{col} by cohort (stacked)")
                ax.set_xlabel(col); ax.set_ylabel("Count")
                plt.tight_layout(); plt.show()

            elif _comp_pref == "stacked_bar_pct":
                _perc = _tab.div(_tab.sum(axis=1), axis=0) * 100
                ax = _perc.plot(kind='bar', stacked=True, rot=0, figsize=(10, 4))
                ax.set_title(f"{col} by cohort (100% stacked)")
                ax.set_xlabel(col); ax.set_ylabel("Percent")
                plt.tight_layout(); plt.show()

            elif _comp_pref == "heatmap":
                _perc = _tab.div(_tab.sum(axis=1), axis=0) * 100
                import numpy as np
                fig, ax = plt.subplots(figsize=(8, max(3, 0.35*len(_perc))))
                im = ax.imshow(_perc.values, aspect='auto')
                ax.set_xticks(range(_perc.shape[1])); ax.set_xticklabels(_perc.columns, rotation=0)
                ax.set_yticks(range(_perc.shape[0])); ax.set_yticklabels(_perc.index)
                ax.set_title(f"{col} by cohort — % heatmap")
                for i in range(_perc.shape[0]):
                    for j in range(_perc.shape[1]):
                        ax.text(j, i, f"{{_perc.values[i, j]:.1f}}%", ha="center", va="center")
                fig.colorbar(im, ax=ax, label="%")
                plt.tight_layout(); plt.show()

            else:  # counts_bar (default)
                ax = _tab.sum(axis=1).plot(kind='bar', rot=0, figsize=(10, 3))
                ax.set_title(f"{col}: total counts (both cohorts)")
                ax.set_xlabel(col); ax.set_ylabel("Count")
                plt.tight_layout(); plt.show()
        """.lstrip()
        return snippet

    # --------------- CASE B: facet-by (categories/bins) ---------------
    if facet:
        facet_col, how = facet
        # Build facet series
        if pd.api.types.is_numeric_dtype(df[facet_col]):
            if how == "bmi":
                facet_series = _bmi_bins(df[facet_col])
            else:
                # generic numeric bins: 3 equal-width bins by default
                facet_series = pd.cut(df[facet_col].astype(float), bins=3)
        else:
            facet_series = df[facet_col].astype(str)

        # Choose pie dimension (categorical to count inside each facet)
        pie_dim = None
        for c in cats:
            if c in df.columns and _is_cat(c):
                pie_dim = c; break
        if pie_dim is None:
            pie_dim = _fallback_cat()
        if pie_dim is None:
            return code

        snippet = f"""
        import math
        import pandas as pd
        import matplotlib.pyplot as plt

        df = df.copy()
        _preferred = "{facet_col}" if "{facet_col}" in df.columns else None

        def _select_facet_col(df, preferred=None):
            if preferred is not None:
                return preferred
            # Prefer low-cardinality categoricals (readable pies/grids)
            cat_cols = [
                c for c in df.columns
                if (df[c].dtype == 'object' or str(df[c].dtype).startswith('category'))
                and df[c].nunique() > 1 and df[c].nunique() <= 20
            ]
            if cat_cols:
                cat_cols.sort(key=lambda c: df[c].nunique())
                return cat_cols[0]
            # Else fall back to first usable numeric
            num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 1]
            return num_cols[0] if num_cols else None

        _facet_col = _select_facet_col(df, _preferred)

        if _facet_col is None:
            # Nothing suitable → single facet keeps pipeline alive
            df["__facet__"] = "All"
        else:
            s = df[_facet_col]
            if pd.api.types.is_numeric_dtype(s):
                # Robust numeric binning: quantiles first, fallback to equal-width
                uniq = pd.Series(s).dropna().nunique()
                q = 3 if uniq < 10 else 4 if uniq < 30 else 5
                try:
                    df["__facet__"] = pd.qcut(s.astype(float), q=q, duplicates="drop")
                except Exception:
                    df["__facet__"] = pd.cut(s.astype(float), bins=q)
            else:
                # Cap long tails; keep top categories
                vc = s.astype(str).value_counts()
                keep = vc.index[:{top_n}]
                df["__facet__"] = s.astype(str).where(s.astype(str).isin(keep), other="Other")

        levels = [str(x) for x in df["__facet__"].dropna().unique().tolist()]
        levels = [x for x in levels if x != "nan"]
        levels.sort()

        m = len(levels)
        cols = 3 if m >= 3 else m or 1
        rows = int(math.ceil(m / cols))

        fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(4*cols, 4*rows))
        if not isinstance(axes, (list, np.ndarray)):
            axes = np.array([[axes]])
        axes = axes.reshape(rows, cols)

        for i, lvl in enumerate(levels):
            r, c = divmod(i, cols)
            ax = axes[r, c]
            s = (df.loc[df["__facet"].astype(str) == str(lvl), "{pie_dim}"]
                .astype(str).value_counts().nlargest({top_n}))
            if len(s) > 0:
                ax.pie(s.values, labels=[str(x) for x in s.index],
                    autopct='%1.1f%%', startangle=90, counterclock=False)
            ax.set_title(f"{pie_dim} — {{lvl}}"); ax.axis('equal')

        # hide any empty subplots
        for j in range(m, rows*cols):
            r, c = divmod(j, cols)
            axes[r, c].axis("off")

        plt.tight_layout(); plt.show()

        # --- companion visual (adaptive) ---
        _comp_pref = "{_comp_pref}"
        # build contingency table: pie_dim x facet
        _tab = (df[["__facet__", "{pie_dim}"]]
          .dropna()
          .astype({{"__facet__": str, "{pie_dim}": str}})
          .value_counts()
          .unstack(level="__facet__")
          .fillna(0))

        # keep top categories by overall size
        _tab = _tab.loc[_tab.sum(axis=1).sort_values(ascending=False).index[:{top_n}]]

        if _comp_pref == "grouped_bar":
            ax = _tab.T.plot(kind="bar", rot=0, figsize=(max(8, 1.2*len(_tab.columns)), 4))
            ax.set_title("{pie_dim} by {facet_col} (grouped)")
            ax.set_xlabel("{facet_col}"); ax.set_ylabel("Count")
            plt.tight_layout(); plt.show()

        elif _comp_pref == "stacked_bar":
            ax = _tab.T.plot(kind="bar", stacked=True, rot=0, figsize=(max(8, 1.2*len(_tab.columns)), 4))
            ax.set_title("{pie_dim} by {facet_col} (stacked)")
            ax.set_xlabel("{facet_col}"); ax.set_ylabel("Count")
            plt.tight_layout(); plt.show()

        elif _comp_pref == "stacked_bar_pct":
            _perc = _tab.div(_tab.sum(axis=0), axis=1) * 100  # column-normalised to 100%
            ax = _perc.T.plot(kind="bar", stacked=True, rot=0, figsize=(max(8, 1.2*len(_perc.columns)), 4))
            ax.set_title("{pie_dim} by {facet_col} (100% stacked)")
            ax.set_xlabel("{facet_col}"); ax.set_ylabel("Percent")
            plt.tight_layout(); plt.show()

        elif _comp_pref == "heatmap":
            _perc = _tab.div(_tab.sum(axis=0), axis=1) * 100
            import numpy as np
            fig, ax = plt.subplots(figsize=(max(6, 0.9*len(_perc.columns)), max(4, 0.35*len(_perc))))
            im = ax.imshow(_perc.values, aspect='auto')
            ax.set_xticks(range(_perc.shape[1])); ax.set_xticklabels(_perc.columns, rotation=0)
            ax.set_yticks(range(_perc.shape[0])); ax.set_yticklabels(_perc.index)
            ax.set_title("{pie_dim} by {facet_col} — % heatmap")
            for i in range(_perc.shape[0]):
                for j in range(_perc.shape[1]):
                    ax.text(j, i, f"{{_perc.values[i, j]:.1f}}%", ha="center", va="center")
            fig.colorbar(im, ax=ax, label="%")
            plt.tight_layout(); plt.show()

        else:  # counts_bar (default denominators)
            _counts = df["__facet"].value_counts()
            ax = _counts.plot(kind="bar", rot=0, figsize=(6, 3))
            ax.set_title("Counts by {facet_col}")
            ax.set_xlabel("{facet_col}"); ax.set_ylabel("Count")
            plt.tight_layout(); plt.show()

        """.lstrip()
        return snippet

    # --------------- CASE C: single pie ---------------
    chosen = None
    for c in cats:
        if c in df.columns and _is_cat(c):
            chosen = c; break
    if chosen is None:
        chosen = _fallback_cat()

    if chosen:
        snippet = f"""
        import matplotlib.pyplot as plt
        counts = df['{chosen}'].astype(str).value_counts().nlargest({top_n})
        fig, ax = plt.subplots()
        if len(counts) > 0:
            ax.pie(counts.values, labels=[str(i) for i in counts.index],
                autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.set_title('Distribution of {chosen} (top {top_n})')
        ax.axis('equal')
        plt.show()
        """.lstrip()
        return snippet

    # numeric last resort
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if num_cols:
        col = num_cols[0]
        snippet = f"""
        import pandas as pd
        import matplotlib.pyplot as plt
        bins = pd.qcut(df['{col}'], q=5, duplicates='drop')
        counts = bins.value_counts().sort_index()
        fig, ax = plt.subplots()
        if len(counts) > 0:
            ax.pie(counts.values, labels=[str(i) for i in counts.index],
                autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.set_title('Distribution of {col} (binned)')
        ax.axis('equal')
        plt.show()
        """.lstrip()
        return snippet

    return code


def patch_fix_seaborn_palette_calls(code: str) -> str:
    """
    Removes seaborn `palette=` when no `hue=` is present in the same call.
    Fixes FutureWarning: 'Passing `palette` without assigning `hue` ...'.
    """
    if "sns." not in code:
        return code

    # Targets common seaborn plotters
    funcs = r"(boxplot|barplot|countplot|violinplot|stripplot|swarmplot|histplot|kdeplot)"
    pattern = re.compile(rf"(sns\.{funcs}\s*\()([^)]*)\)", re.DOTALL)

    def _fix_call(m):
        head, inner = m.group(1), m.group(2)
        # If there's already hue=, keep as is
        if re.search(r"(?<!\w)hue\s*=", inner):
            return f"{head}{inner})"
        # Otherwise remove palette=... safely (and any adjacent comma spacing)
        inner2 = re.sub(r",\s*palette\s*=\s*[^,)\n]+", "", inner)
        inner2 = re.sub(r"\bpalette\s*=\s*[^,)\n]+\s*,\s*", "", inner2)
        inner2 = re.sub(r"\s*,\s*\)", ")", f"{inner2})")[:-1]  # clean trailing comma before ')'
        return f"{head}{inner2})"

    return pattern.sub(_fix_call, code)


def patch_quiet_specific_warnings(code: str) -> str:
    """
    Inserts targeted warning filters (not blanket ignores).
    - seaborn palette/hue deprecation
    - python-dotenv parse chatter
    """
    prelude = (
        "import warnings\n"
        "warnings.filterwarnings(\n"
        "    'ignore', message=r'.*Passing `palette` without assigning `hue`.*', category=FutureWarning)\n"
        "warnings.filterwarnings(\n"
        "    'ignore', message=r'python-dotenv could not parse statement.*')\n"
    )
    # If warnings already imported once, just add filters; else insert full prelude.
    if "import warnings" in code:
        code = re.sub(
            r"(import warnings[^\n]*\n)",
            lambda m: m.group(1) + prelude.replace("import warnings\n", ""),
            code,
            count=1
        )

    else:
        # place after first import block if possible
        m = re.search(r"^(?:from\s+\S+\s+import\s+.+|import\s+\S+).*\n+", code, flags=re.MULTILINE)
        if m:
            idx = m.end()
            code = code[:idx] + prelude + code[idx:]
        else:
            code = prelude + code
    return code


def _norm_col_name(s: str) -> str:
    """normalise a column name: lowercase + strip non-alphanumerics."""
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def _first_present(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """return the actual df column that matches any candidate (after normalisation)."""
    norm_map = {_norm_col_name(c): c for c in df.columns}
    for cand in candidates:
        hit = norm_map.get(_norm_col_name(cand))
        if hit is not None:
            return hit
    return None


def _ensure_canonical_alias(df: pd.DataFrame, target: str, aliases: list[str]) -> tuple[pd.DataFrame, bool]:
    """
    If any alias exists, materialise a canonical copy at `target` (don’t drop the original).
    Returns (df, found_bool).
    """
    if target in df.columns:
        return df, True
    col = _first_present(df, [target, *aliases])
    if col is None:
        return df, False
    df[target] = df[col]
    return df, True


def strip_python_dotenv(code: str) -> str:
    """
    Remove any use of python-dotenv from generated code, including:
      - single and multi-line 'from dotenv import ...'
      - 'import dotenv' (with or without alias) and calls via any alias
      - load_dotenv/find_dotenv/dotenv_values calls (bare or prefixed)
      - IPython magics (%load_ext dotenv, %dotenv, %env …)
      - shell installs like '!pip install python-dotenv'
    """
    original = code

    # 0) Kill IPython magics & shell installs referencing dotenv
    code = re.sub(r"^\s*%load_ext\s+dotenv\s*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*%dotenv\b.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*%env\b.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*!\s*pip\s+install\b.*dotenv.*$", "", code, flags=re.IGNORECASE | re.MULTILINE)

    # 1) Remove single-line 'from dotenv import ...'
    code = re.sub(r"^\s*from\s+dotenv\s+import\s+.*$", "", code, flags=re.MULTILINE)

    # 2) Remove multi-line 'from dotenv import ( ... )' blocks
    code = re.sub(
        r"^\s*from\s+dotenv\s+import\s*\([\s\S]*?\)\s*$",
        "",
        code,
        flags=re.MULTILINE,
    )

    # 3) Remove 'import dotenv' (with optional alias). Capture alias names.
    aliases = re.findall(r"^\s*import\s+dotenv\s+as\s+([A-Za-z_][A-Za-z0-9_]*)\s*$",
                         code, flags=re.MULTILINE)
    code = re.sub(r"^\s*import\s+dotenv\s*(?:as\s+[A-Za-z_][A-Za-z0-9_]*)?\s*$",
                  "", code, flags=re.MULTILINE)

    # 4) Remove calls to load_dotenv / find_dotenv / dotenv_values with any prefix
    #    e.g., load_dotenv(...), dotenv.load_dotenv(...), dtenv.load_dotenv(...)
    fn_names = r"(?:load_dotenv|find_dotenv|dotenv_values)"
    # bare calls
    code = re.sub(rf"^\s*{fn_names}\s*\([^)]*\)\s*$", "", code, flags=re.MULTILINE)
    # dotted calls with any identifier prefix (alias or module)
    code = re.sub(rf"^\s*[A-Za-z_][A-Za-z0-9_]*\s*\.\s*{fn_names}\s*\([^)]*\)\s*$",
                  "", code, flags=re.MULTILINE)

    # 5) If any alias imported earlier slipped through (method chains etc.), remove lines using that alias.
    for al in aliases:
        code = re.sub(rf"^\s*{al}\s*\.\s*\w+\s*\([^)]*\)\s*$", "", code, flags=re.MULTILINE)

    # 6) Tidy excess blank lines
    code = re.sub(r"\n{3,}", "\n\n", code).strip("\n") + "\n"
    return code


def fix_predict_calls_records_arg(code: str) -> str:
    """
    If generated code calls predict_* with a list-of-dicts via .to_dict('records')
    (or orient='records'), strip the .to_dict(...) so a DataFrame is passed instead.
    Works line-by-line to avoid over-rewrites elsewhere.
    Examples fixed:
      predict_patient(X_test.iloc[:5].to_dict('records'))
      predict_risk(df.head(3).to_dict(orient="records"))
    → predict_patient(X_test.iloc[:5])
    """
    fixed_lines = []
    for line in code.splitlines():
        if "predict_" in line and "to_dict" in line and "records" in line:
            line = re.sub(
                r"\.to_dict\s*\(\s*(?:orient\s*=\s*)?['\"]records['\"]\s*\)",
                "",
                line
            )
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def fix_fstring_backslash_paths(code: str) -> str:
    """
    Fix bad f-strings like: f"...{out_dir\\plots\\img.png}..."
    → f"...{os.path.join(out_dir, r'plots\\img.png')}"
    Only touches f-strings that contain a backslash path inside {...}.
    """
    def _fix_line(line: str) -> str:
        # quick check: only f-strings need scanning
        if not (("f\"" in line) or ("f'" in line) or ("f\"\"\"" in line) or ("f'''" in line)):
            return line
        # {var\rest-of-path} where var can be dotted (e.g., cfg.out)
        pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_\.]*)\\([^}]+)\}")
        def repl(m):
            left = m.group(1)
            right = m.group(2).strip().replace('"', '\\"')
            return "{os.path.join(" + left + ', r"' + right + '")}'
        return pattern.sub(repl, line)

    return "\n".join(_fix_line(ln) for ln in code.splitlines())


def ensure_os_import(code: str) -> str:
    """
    If os.path.join is used but 'import os' is missing, inject it at the top.
    """
    needs = "os.path.join(" in code
    has_import_os = re.search(r"^\s*import\s+os\b", code, flags=re.MULTILINE) is not None
    has_from_os = re.search(r"^\s*from\s+os\s+import\b", code, flags=re.MULTILINE) is not None
    if needs and not (has_import_os or has_from_os):
        return "import os\n" + code
    return code


def fix_seaborn_boxplot_nameerror(code: str) -> str:
    """
    Fix bad calls like: sns.boxplot(boxplot)
    Heuristic:
      - If plot_df + FH_status + var exist → sns.boxplot(data=plot_df, x='FH_status', y=var, ax=ax)
      - Else if plot_df + var → sns.boxplot(data=plot_df, y=var, ax=ax)
      - Else if plot_df only → sns.boxplot(data=plot_df, ax=ax)
      - Else → sns.boxplot(ax=ax)
    Ensures a matplotlib Axes 'ax' exists.
    """
    pattern = re.compile(r"^\s*sns\.boxplot\s*\(\s*boxplot\s*\)\s*$", re.MULTILINE)
    if not pattern.search(code):
        return code

    has_plot_df = re.search(r"\bplot_df\b", code) is not None
    has_var     = re.search(r"\bvar\b", code) is not None
    has_fh      = bool(re.search(r"['\"]FH_status['\"]", code) or re.search(r"\bFH_status\b", code))

    if has_plot_df and has_var and has_fh:
        replacement = "sns.boxplot(data=plot_df, x='FH_status', y=var, ax=ax)"
    elif has_plot_df and has_var:
        replacement = "sns.boxplot(data=plot_df, y=var, ax=ax)"
    elif has_plot_df:
        replacement = "sns.boxplot(data=plot_df, ax=ax)"
    else:
        replacement = "sns.boxplot(ax=ax)"

    fixed = pattern.sub(replacement, code)

    # Ensure 'fig, ax = plt.subplots(...)' exists
    if "ax=" in replacement and not re.search(r"\bfig\s*,\s*ax\s*=\s*plt\.subplots\s*\(", fixed):
        # Insert right before the first seaborn call
        m = re.search(r"^\s*sns\.", fixed, flags=re.MULTILINE)
        insert_at = m.start() if m else 0
        fixed = fixed[:insert_at] + "fig, ax = plt.subplots(figsize=(8,4))\n" + fixed[insert_at:]

    return fixed


def fix_seaborn_barplot_nameerror(code: str) -> str:
    """
    Fix bad calls like: sns.barplot(barplot)
    Strategy mirrors boxplot fixer: prefer data=plot_df with x/y if available,
    otherwise degrade safely to an empty call on an existing Axes.
    """
    import re
    pattern = re.compile(r"^\s*sns\.barplot\s*\(\s*barplot\s*\)\s*$", re.MULTILINE)
    if not pattern.search(code):
        return code

    has_plot_df = re.search(r"\bplot_df\b", code) is not None
    has_var     = re.search(r"\bvar\b", code) is not None
    has_fh      = bool(re.search(r"['\"]FH_status['\"]", code) or re.search(r"\bFH_status\b", code))

    if has_plot_df and has_var and has_fh:
        replacement = "sns.barplot(data=plot_df, x='FH_status', y=var, ax=ax)"
    elif has_plot_df and has_var:
        replacement = "sns.barplot(data=plot_df, y=var, ax=ax)"
    elif has_plot_df:
        replacement = "sns.barplot(data=plot_df, ax=ax)"
    else:
        replacement = "sns.barplot(ax=ax)"

    # ensure an Axes 'ax' exists (no-op if already present)
    if "ax =" not in code:
        code = "import matplotlib.pyplot as plt\nfig, ax = plt.subplots(figsize=(6,4))\n" + code

    return pattern.sub(replacement, code)


def parse_and_format_ml_pipeline(raw_text: str) -> tuple[str, str, str]:
    """
    Parses the raw text to extract and format the 'refined question', 
    'intents (tasks)', and 'chronology of tasks' sections.
    Args:
        raw_text: The complete input string containing the ML pipeline structure.
    Returns:
        A tuple containing: 
        (formatted_question_str, formatted_intents_str, formatted_chronology_str)
    """
    # --- 1. Regex Pattern to Extract Sections ---
    # The pattern uses capturing groups (?) to look for the section headers 
    # (e.g., 'refined question:') and captures all the content until the next 
    # section header or the end of the string. re.DOTALL is crucial for '.' to match newlines.
    
    pattern = re.compile(
        r"refined question:(?P<question>.*?)"
        r"intents \(tasks\):(?P<intents>.*?)"
        r"Chronology of tasks:(?P<chronology>.*)",
        re.IGNORECASE | re.DOTALL
    )
    
    match = pattern.search(raw_text)
    
    if not match:
        raise ValueError("Input text structure does not match the expected pattern.")

    # --- 2. Extract Content ---
    question_content = match.group('question').strip()
    intents_content = match.group('intents').strip()
    chronology_content = match.group('chronology').strip()

    # --- 3. Formatting Functions ---

    def format_question(content):
        """Formats the Refined Question section."""
        # Clean up leading/trailing whitespace and ensure clean paragraphs
        content = content.strip().replace('\n', ' ').replace('  ', ' ')
        
        # Simple formatting using Markdown headers and bolding
        formatted = (
            # "## 1. Project Goal and Objectives\n\n"
            "<b> Refined Question:</b>\n"
            f"{content}\n"
        )
        return formatted

    def format_intents(content):
        """Formats the Intents (Tasks) section as a structured list."""
        # Use regex to find and format each numbered task
        # It finds 'N. **Text** - ...' and breaks it down.
        
        tasks = []
        # Pattern: N. **Text** - Content (including newlines, non-greedy)
        # We need to explicitly handle the list items starting with '-' within the content
        task_pattern = re.compile(r'(\d+\. \*\*.*?\*\*.*?)(?=\n\d+\. \*\*|\Z)', re.DOTALL)
        
        # Split the content by lines and join tasks back into clean strings
        raw_tasks = [m.group(1).strip() for m in task_pattern.finditer(content)]
        
        for task in raw_tasks:
            # Replace the initial task number and **Heading** with a Heading 3
            task = re.sub(r'^\d+\. (\*\*.*?\*\*)', r'### \1', task, count=1, flags=re.MULTILINE)
            
            # Replace list markers (' - ') with Markdown bullets ('* ') for clarity
            task = task.replace('\n - ', '\n* ').replace('- ', '* ', 1) 
            tasks.append(task)
            
        formatted_tasks = "\n\n".join(tasks)

        return (
            "\n---\n"
            "## 2. Methodology and Tasks\n\n"
            f"{formatted_tasks}\n"
        )

    def format_chronology(content):
        """Formats the Chronology section."""
        # Uses the given LaTeX format
        content = content.strip().replace(' ', ' \rightarrow ')
        formatted = (
            "\n---\n"
            "## 3. Chronology of Tasks\n"
            f"$$\\text{{{content}}}$$"
        )
        return formatted

    # --- 4. Format and Return ---
    formatted_question = format_question(question_content)
    formatted_intents = format_intents(intents_content)
    formatted_chronology = format_chronology(chronology_content)

    return formatted_question, formatted_intents, formatted_chronology


def generate_full_report(formatted_question: str, formatted_intents: str, formatted_chronology: str) -> str:
    """Combines all formatted parts into a final report string."""
    return (
        "# 🔬 Machine Learning Pipeline for Predicting Family History of Diabetes\n\n"
        f"{formatted_question}\n"
        f"{formatted_intents}\n"
        f"{formatted_chronology}\n"
    )


def fix_confusion_matrix_for_multilabel(code: str) -> str:
    """
    Replace ConfusionMatrixDisplay.from_estimator(...) usages with
    from_predictions(...) which works for multi-label loops without requiring
    the estimator to expose _estimator_type.
    """
    return re.sub(
        r"ConfusionMatrixDisplay\.from_estimator\(([^,]+),\s*([^,]+),\s*([^)]+)\)",
        r"ConfusionMatrixDisplay.from_predictions(\3, \1.predict(\2))",
        code
    )


def smx_auto_title_plots(ctx=None, fallback="Analysis"):
    """
    Ensure every Matplotlib/Seaborn Axes has a title.
    Uses refined_question -> askai_question -> fallback.
    Only sets a title if it's currently empty.
    """
    import matplotlib.pyplot as plt

    def _all_figures():
        try:
            from matplotlib._pylab_helpers import Gcf
            return [fm.canvas.figure for fm in Gcf.get_all_fig_managers()]
        except Exception:
            # Best effort fallback
            nums = plt.get_fignums()
            return [plt.figure(n) for n in nums] if nums else []

    # Choose a concise title
    title = None
    if isinstance(ctx, dict):
        title = ctx.get("refined_question") or ctx.get("askai_question")
    title = (str(title).strip().splitlines()[0][:120]) if title else fallback

    for fig in _all_figures():
        for ax in getattr(fig, "axes", []):
            try:
                if not (ax.get_title() or "").strip():
                    ax.set_title(title)
            except Exception:
                pass
        try:
            fig.tight_layout()
        except Exception:
            pass


def patch_fix_sentinel_plot_calls(code: str) -> str:
    """
    Normalise 'sentinel first-arg' calls so wrappers can pick sane defaults.
      SB_barplot(barplot)            -> SB_barplot()
      SB_barplot(barplot, ...)       -> SB_barplot(...)
      sns.barplot(barplot)           -> SB_barplot()
      sns.barplot(barplot, ...)      -> SB_barplot(...)
    Same for: histplot, boxplot, lineplot, countplot, heatmap, pairplot, scatterplot.
    """
    names = ['histplot','boxplot','barplot','lineplot','countplot','heatmap','pairplot','scatterplot']
    for n in names:
        # SB_* with sentinel as the first arg (with or without trailing args)
        code = re.sub(rf"\bSB_{n}\s*\(\s*{n}\s*\)", f"SB_{n}()", code)
        code = re.sub(rf"\bSB_{n}\s*\(\s*{n}\s*,", f"SB_{n}(", code)
        # sns.* with sentinel as the first arg → route to SB_* (so our wrappers handle it)
        code = re.sub(rf"\bsns\.{n}\s*\(\s*{n}\s*\)", f"SB_{n}()", code)
        code = re.sub(rf"\bsns\.{n}\s*\(\s*{n}\s*,", f"SB_{n}(", code)
    return code


def patch_rmse_calls(code: str) -> str:
    """
    Make RMSE robust across sklearn versions.
    - Replace mean_squared_error(..., squared=False) -> _SMX_rmse(...)
    - Wrap any remaining mean_squared_error(...) calls with _SMX_call for safety.
    """
    import re
    # (a) Specific RMSE pattern
    code = re.sub(
        r"\bmean_squared_error\s*\(\s*(.+?)\s*,\s*squared\s*=\s*False\s*\)",
        r"_SMX_rmse(\1)",
        code,
        flags=re.DOTALL
    )
    # (b) Guard any other MSE calls
    code = re.sub(r"\bmean_squared_error\s*\(", r"_SMX_call(mean_squared_error, ", code)
    return code
