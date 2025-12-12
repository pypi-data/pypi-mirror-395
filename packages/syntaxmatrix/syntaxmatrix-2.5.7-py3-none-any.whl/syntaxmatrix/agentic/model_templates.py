# syntaxmatrix/model_templates.py
from textwrap import dedent


def classification(df, target=None):
    code = dedent("""
        # ==== CLASSIFICATION BASELINE (titles + shared SMX_SAMPLE_CAP) ====
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            classification_report, confusion_matrix, roc_curve, auc,
            precision_recall_curve, average_precision_score, accuracy_score,
            f1_score, recall_score, precision_score
        )

        _work = df.copy()

        # --- 0) Sample cap (from PREFACE) ---
        try:
            CAP = int(SMX_SAMPLE_CAP)
        except Exception:
            CAP = 5000
        if len(_work) > CAP:
            _work = _work.sample(n=CAP, random_state=42)

        # --- 1) Choose target (use hint if valid, else heuristic) ---
        _hint = __SMX_TARGET_HINT__
        target = _hint if (_hint is not None and str(_hint) in _work.columns) else None
        if target is None:
            prefs = ['target','label','class','y','outcome','churn','default','is_fraud','clicked','purchased']
            for c in prefs:
                if c in _work.columns:
                    target = c; break
        if target is None:
            # choose low-cardinality column
            cand = [(c, _work[c].nunique(dropna=True)) for c in _work.columns]
            cand = [c for c, k in cand if k <= 20 and c.lower() not in ('id','uuid')]
            target = cand[-1] if cand else None

        if target is None:
            show("No obvious classification target found.", title="Classification")
        elif _work[target].nunique(dropna=True) < 2:
            show(f"Target '{target}' has fewer than two classes.", title="Classification")
        else:
            X = _work.drop(columns=[target])
            y = _work[target].astype(str)

            num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = X.select_dtypes(include=["object","category","string","bool"]).columns.tolist()

            # robust OneHot across sklearn versions (uses PREFACE helper if present)
            try:
                enc = _SMX_OHE()
            except Exception:
                enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

            pre = ColumnTransformer(
                transformers=[
                    ("num", Pipeline([("scaler", StandardScaler())]), num_cols) if num_cols else ("num","drop",[]),
                    ("cat", enc, cat_cols) if cat_cols else ("cat","drop",[]),
                ],
                remainder="drop"
            )

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
            )

            clf = Pipeline([
                ("pre", pre),
                ("est", LogisticRegression(max_iter=1000, class_weight="balanced"))
            ])
            clf.fit(X_train, y_train)

            y_pred = clf.predict(X_test)
            try:
                proba = clf.predict_proba(X_test)
                y_score = proba.max(axis=1)
            except Exception:
                proba, y_score = None, None

            # --- 2) Tables with explicit titles ---
            cr = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
            show(pd.DataFrame(cr).transpose(), title="Classification report")

            # Confusion matrix (robust labels)
            labels_list = sorted(list(pd.unique(y)))
            cm = confusion_matrix(y_test, y_pred, labels=labels_list)
            index = [f"true:{str(lbl)}" for lbl in labels_list]
            columns = [f"pred:{str(lbl)}" for lbl in labels_list]
            cm_df = pd.DataFrame(cm, index=index, columns=columns)
            show(cm_df, title="Confusion matrix")

            summary = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision_macro": float(precision_score(y_test, y_pred, average="macro", zero_division=0)),
                "recall_macro": float(recall_score(y_test, y_pred, average="macro", zero_division=0)),
                "f1_macro": float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
                "classes": int(len(labels_list)),
                "rows_used": int(len(_work))
            }
            show(summary, title="Metrics summary")

            # --- 3) ROC / PR curves for binary (best-effort) ---
            if proba is not None and len(labels_list) == 2:
                pos = labels_list[1]
                y_bin = (y_test == pos).astype(int)
                y_prob = proba[:, 1]
                fpr, tpr, _ = roc_curve(y_bin, y_prob)
                roc_auc = auc(fpr, tpr)

                fig, ax = plt.subplots(figsize=(6,5))
                ax.plot(fpr, tpr)
                ax.plot([0,1],[0,1], linestyle="--")
                ax.set_title(f"ROC curve (AUC={roc_auc:.3f})")
                ax.set_xlabel("FPR"); ax.set_ylabel("TPR")
                plt.tight_layout(); plt.show()

                prec, rec, _ = precision_recall_curve(y_bin, y_prob)
                ap = average_precision_score(y_bin, y_prob)
                fig2, ax2 = plt.subplots(figsize=(6,4))
                ax2.plot(rec, prec)
                ax2.set_title(f"Precision–Recall (AP={ap:.3f})")
                ax2.set_xlabel("Recall"); ax2.set_ylabel("Precision")
                plt.tight_layout(); plt.show()

            # --- 4) Predictions sample (captioned) ---
            out = X_test.copy()
            out["_true"] = y_test.values
            out["_pred"] = y_pred
            if y_score is not None:
                out["_score"] = y_score
            show(out.head(20), title="Predictions (sample)")
    """)
    return code.replace("__SMX_TARGET_HINT__", repr(target))


def regression(df, target=None):
    code = dedent("""
        # ==== REGRESSION BASELINE (titles + shared SMX_SAMPLE_CAP) ====
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.linear_model import Ridge
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        _work = df.copy()
        try:
            CAP = int(SMX_SAMPLE_CAP)
        except Exception:
            CAP = 5000
        if len(_work) > CAP:
            _work = _work.sample(n=CAP, random_state=42)

        # target pick (hint first)
        _hint = __SMX_TARGET_HINT__
        target = _hint if (_hint is not None and str(_hint) in _work.columns) else None

        if target is None:
            num_cols_all = _work.select_dtypes(include=[np.number]).columns.tolist()
            for c in ['target','y','price','amount','value','score','sales','revenue']:
                if c in num_cols_all:
                    target = c; break
            if target is None and num_cols_all:
                target = num_cols_all[-1]

        if target is None:
            show("No numeric target found for regression.", title="Regression")
        else:
            X = _work.drop(columns=[target]); y = _work[target].astype(float)

            num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = X.select_dtypes(include=["object","category","string","bool"]).columns.tolist()

            try:
                enc = _SMX_OHE()
            except Exception:
                enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

            pre = ColumnTransformer(
                transformers=[
                    ("num", Pipeline([("scaler", StandardScaler())]), num_cols) if num_cols else ("num","drop",[]),
                    ("cat", enc, cat_cols) if cat_cols else ("cat","drop",[]),
                ],
                remainder="drop"
            )

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = Pipeline([("pre", pre), ("est", Ridge(alpha=1.0, random_state=42))])
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            rmse = float(np.sqrt(mse))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            show({"MAE": float(mae), "MSE": float(mse), "RMSE": rmse, "R²": float(r2), "rows_used": int(len(_work))},
                 title="Regression metrics")

            fig, ax = plt.subplots(figsize=(6,5))
            ax.scatter(y_test, y_pred, s=18, alpha=0.7)
            ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle="--")
            ax.set_title("Parity plot (y vs ŷ)"); ax.set_xlabel("Actual"); ax.set_ylabel("Predicted")
            plt.tight_layout(); plt.show()

            resid = y_test - y_pred
            fig2, ax2 = plt.subplots(figsize=(6,4))
            ax2.scatter(y_pred, resid, s=16, alpha=0.7)
            ax2.axhline(0.0, linestyle="--")
            ax2.set_title("Residuals vs predicted"); ax2.set_xlabel("Predicted"); ax2.set_ylabel("Residual")
            plt.tight_layout(); plt.show()

            out = X_test.copy(); out["_actual"] = y_test.values; out["_pred"] = y_pred; out["_residual"] = resid
            show(out.head(20), title="Predictions (sample)")
    """)
    return code.replace("__SMX_TARGET_HINT__", repr(target))


def multilabel_classification(df, label_cols):
    """
    Baseline multi-label pipeline:
    - X: numeric features only (excludes label_cols)
    - y: df[label_cols] (2D binary frame)
    - Model: OneVsRest(LogisticRegression)
    - Metrics: subset accuracy, hamming loss, micro/macro F1, per-label ROC AUC
    - Confusion matrices: from_predictions per label (no estimator wrapper)
    """
    return dedent(f"""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.multiclass import OneVsRestClassifier
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import (
            accuracy_score, hamming_loss, f1_score, roc_auc_score,
            classification_report, ConfusionMatrixDisplay
        )

        LABEL_COLS = {list(label_cols)}

        # X = numeric features only, drop labels
        X = df.drop(columns=LABEL_COLS).select_dtypes(include=['number','bool']).copy()
        y = df[LABEL_COLS].astype(int).copy()

        if X.empty:
            raise ValueError("No numeric features available for multi-label classification.")
        if y.shape[1] < 2:
            raise ValueError("Need at least two label columns for multi-label classification.")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y.sum(axis=1) if y.sum(axis=1).nunique()>1 else None
        )

        pipeline = Pipeline(steps=[
            ("scaler", StandardScaler(with_mean=False)),
            ("clf", OneVsRestClassifier(LogisticRegression(max_iter=200, n_jobs=None)))
        ])

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        # Probas for AUC (fallback to zeros if not available)
        try:
            y_proba = pipeline.predict_proba(X_test)
            y_proba = np.column_stack([p[:,1] if p.ndim==2 else p for p in y_proba])
        except Exception:
            y_proba = np.zeros_like(y_pred, dtype=float)

        # Aggregate metrics
        metrics_row = {{
            "accuracy": accuracy_score(y_test, y_pred),
            "hamming_loss": hamming_loss(y_test, y_pred),
            "f1_micro": f1_score(y_test, y_pred, average="micro", zero_division=0),
            "f1_macro": f1_score(y_test, y_pred, average="macro", zero_division=0),
        }}
        # macro ROC AUC if we have probabilities
        try:
            metrics_row["roc_auc_macro"] = roc_auc_score(y_test, y_proba, average="macro")
        except Exception:
            metrics_row["roc_auc_macro"] = np.nan

        show(pd.DataFrame([metrics_row]))

        # Per-label report and ROC AUC
        report_rows = []
        for j, col in enumerate(LABEL_COLS):
            try:
                auc = roc_auc_score(y_test.iloc[:, j], y_proba[:, j]) if y_proba.size else np.nan
            except Exception:
                auc = np.nan
            report = classification_report(
                y_test.iloc[:, j], y_pred[:, j], output_dict=True, zero_division=0
            )
            report_rows.append({{"label": col, "roc_auc": auc}})
        show(pd.DataFrame(report_rows))

        # Confusion matrices per label — use from_predictions (no estimator wrapper needed)
        n = len(LABEL_COLS)
        ncols = 3 if n >= 3 else n
        nrows = int(np.ceil(n / ncols)) if ncols else 1
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols, 3*nrows))
        axes = axes.ravel() if n > 1 else [axes]
        for i, col in enumerate(LABEL_COLS[:len(axes)]):
            ConfusionMatrixDisplay.from_predictions(
                y_test.iloc[:, i], y_pred[:, i], ax=axes[i], cmap=plt.cm.Blues
            )
            axes[i].set_title(col)
        plt.tight_layout()
        plt.show()
    """)


def eda_overview(df):
    return dedent("""
        # ── Auto-generated EDA overview ───────────────
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
       
        _df = df.copy()
        num_cols = _df.select_dtypes(include=['number', 'bool']).columns.tolist()

        if num_cols:
            summary = _df[num_cols].describe().T.reset_index().rename(columns={'index': 'feature'})
            show(summary)

            sample = _df[num_cols]
            if len(sample) > 500:
                sample = sample.sample(500, random_state=42)

            sns.pairplot(sample)
            plt.tight_layout()
            plt.show()
        else:
            show("No numeric columns available for EDA overview.")
    """)


def eda_correlation(df):
    return dedent("""
        # ── Auto-generated correlation analysis ───────────────
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
       
        _df = df.copy()
        num_cols = _df.select_dtypes(include=['number', 'bool']).columns.tolist()
        if not num_cols:
            raise ValueError("No numeric columns available for correlation analysis.")

        corr = _df[num_cols].corr()
        show(corr)

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=False, cmap="coolwarm", center=0)
        plt.title("Correlation heatmap (numeric features)")
        plt.tight_layout()
        plt.show()
    """)


def anomaly_detection(df):
    return dedent("""
        # ── Auto-generated IsolationForest anomaly detection ─────────────
        import numpy as np
        import pandas as pd
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from IPython.display import display, HTML

        # Split numeric vs categorical for simple preprocessing
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols]

        if len(num_cols) + len(cat_cols) == 0:
            raise ValueError("No usable columns for anomaly detection.")

        preproc = ColumnTransformer(
            transformers=[
                ("num", "passthrough", num_cols),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ],
            remainder="drop",
            verbose_feature_names_out=False,
        )

        model = IsolationForest(
            n_estimators=300,
            contamination="auto",
            random_state=42
        )

        pipe = Pipeline([
            ("prep", preproc),
            ("iso", model),
        ])

        X = df[num_cols + cat_cols].copy()
        pipe.fit(X)

        # More negative = more anomalous in sklearn's score_samples
        scores = pipe.named_steps["iso"].score_samples(pipe.named_steps["prep"].transform(X))
        out = df.copy()
        out["anomaly_score"] = -scores

        # Flag top 5% as anomalies (simple heuristic)
        threshold = np.percentile(out["anomaly_score"], 95)
        out["is_anomaly"] = out["anomaly_score"] >= threshold

        # Show the most anomalous rows
        top = out.sort_values("anomaly_score", ascending=False).head(20)
        display(HTML(top.to_html(index=False)))
    """)


def ts_anomaly_detection(df):
    return dedent("""
        # ==== TIME-SERIES ANOMALY DETECTION ====
        # Prefers STL (statsmodels). If not available, falls back to rolling-MAD.
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt
        
        _df = df.copy()

        # --- 1) Find a datetime column (or use datetime index) ---
        time_col = None
        if isinstance(_df.index, pd.DatetimeIndex):
            _df = _df.reset_index().rename(columns={"index": "timestamp"})
            time_col = "timestamp"
        else:
            # try common names first, then dtype-based
            preferred = [c for c in _df.columns if ("date" in c.lower() or "time" in c.lower())]
            dt_candidates = preferred + _df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
            for c in dt_candidates or _df.columns.tolist():
                try:
                    _df[c] = pd.to_datetime(_df[c], errors="coerce")
                    if _df[c].notna().sum() >= 3:
                        time_col = c
                        break
                except Exception:
                    pass

        if time_col is None:
            show("No timestamp/datetime column found. Provide a column like 'date' or 'timestamp'.")
        else:
            # --- 2) Pick a numeric value column ---
            num_cols = _df.select_dtypes(include=[np.number]).columns.tolist()
            preferred_vals = [c for c in num_cols if any(k in c.lower() for k in ["value","amount","count","y","target"])]
            value_col = preferred_vals[0] if preferred_vals else (num_cols[0] if num_cols else None)

            if value_col is None:
                show("No numeric value column found for time-series analysis.")
            else:
                ts = _df[[time_col, value_col]].dropna().sort_values(time_col).set_index(time_col)

                # --- 3) Infer resample rule (D/W/M) ---
                def _choose_rule(idx):
                    if len(idx) < 3: return "D"
                    # median gap in seconds
                    arr = idx.view("i8")
                    diffs = np.diff(arr) / 1e9 if len(arr) > 1 else np.array([0.0])
                    med = np.median(diffs) if len(diffs) else 0.0
                    day = 86400.0
                    if med <= day: return "D"
                    if med <= 7 * day: return "W"
                    return "M"

                rule = _choose_rule(ts.index.values)
                period_map = {"D": 7, "W": 52, "M": 12}
                period = period_map.get(rule, 7)

                # --- 4) Resample & detect anomalies (STL or fallback) ---
                ts_res = ts.resample(rule).mean().dropna()
                used_statsmodels = False
                try:
                    from statsmodels.tsa.seasonal import STL
                    used_statsmodels = True
                    stl = STL(ts_res[value_col], robust=True, period=period)
                    res = stl.fit()
                    trend = res.trend
                    resid = res.resid
                    seasonal = res.seasonal
                    # robust z-score
                    mad = np.median(np.abs(resid - np.median(resid))) or 1e-8
                    z = np.abs(resid) / (1.4826 * mad)
                    anomalies = z > 3.5
                except Exception:
                    # --- Rolling-MAD fallback (no statsmodels required) ---
                    used_statsmodels = False
                    series = ts_res[value_col]
                    # choose an odd window scaled to series length
                    n = max(7, min(61, (len(series) // 10) * 2 + 1))
                    med = series.rolling(window=n, center=True, min_periods=max(3, n // 3)).median()
                    resid = series - med
                    mad = (np.abs(resid)).rolling(window=n, center=True, min_periods=max(3, n // 3)).median()
                    # robust scale; avoid zeros
                    scale = (1.4826 * mad).replace(0, np.nan)
                    scale = scale.fillna(scale.median() or 1e-8)
                    z = np.abs(resid) / scale
                    anomalies = z > 3.5
                    trend = med
                    seasonal = pd.Series(0.0, index=series.index)

                out = ts_res.copy()
                out["trend"] = trend.reindex(out.index)
                out["resid"] = resid.reindex(out.index)
                out["zscore"] = z.reindex(out.index)
                out["anomaly"] = anomalies.reindex(out.index).astype(bool)

                # --- 5) UI outputs (no prints) ---
                mode_note = "STL (statsmodels)" if used_statsmodels else "Rolling-MAD fallback"
                show({"method": mode_note, "frequency": rule, "period": period, "points": int(out.shape[0]), "anomalies": int(out["anomaly"].sum())})
                show(out[out["anomaly"]].head(30))

                # value + trend + anomalies
                fig, ax = plt.subplots(figsize=(9, 5))
                ax.plot(out.index, out[value_col], label="value")
                ax.plot(out.index, out["trend"], label="trend")
                ax.scatter(out.index[out["anomaly"]], out[value_col][out["anomaly"]], s=40, label="anomaly")
                ax.set_title(f"Time-series anomalies ({mode_note})")
                ax.set_xlabel("time"); ax.set_ylabel(value_col)
                ax.legend(loc="best"); plt.tight_layout(); plt.show()

                # robust z-scores
                fig2, ax2 = plt.subplots(figsize=(9, 3))
                ax2.plot(out.index, out["zscore"])
                ax2.axhline(3.5, linestyle="--")
                ax2.set_title("Robust z-score")
                ax2.set_xlabel("time"); ax2.set_ylabel("z")
                plt.tight_layout(); plt.show()

                # sample of last periods for quick inspection
                show(out.tail(12))
    """)


def dimensionality_reduction(df):
    return dedent("""
        # ── Dimensionality Reduction (PCA + optional t-SNE) ───────────────
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        try:
            from sklearn.manifold import TSNE
            _HAS_TSNE = True
        except Exception:
            _HAS_TSNE = False
        from IPython.display import display, HTML

        _df = df.copy()
        num_cols = _df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) < 2:
            raise ValueError("Need at least 2 numeric columns for PCA. Found: %d" % len(num_cols))

        X = _df[num_cols].astype(float).copy()
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)

        n_comp = int(min(10, Xs.shape[1]))
        pca = PCA(n_components=n_comp)
        Z = pca.fit_transform(Xs)

        # Explained variance table
        evr = pca.explained_variance_ratio_
        cum = np.cumsum(evr)
        stats = pd.DataFrame({
            "component": [f"PC{i+1}" for i in range(n_comp)],
            "explained_variance_ratio": evr,
            "cumulative_variance": cum
        })
        display(HTML("<h4>PCA explained variance</h4>" + stats.to_html(index=False)))

        # 2D scatter of PC1 vs PC2
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(Z[:,0], Z[:,1], s=14, alpha=0.7)
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title("PCA: PC1 vs PC2")
        plt.show()

        # Top absolute loadings for PC1 & PC2
        comps = pd.DataFrame(pca.components_[:2], columns=num_cols, index=["PC1","PC2"]).T
        top1 = comps["PC1"].abs().sort_values(ascending=False).head(10)
        top2 = comps["PC2"].abs().sort_values(ascending=False).head(10)
        display(HTML("<h4>Top |loadings| for PC1</h4>" + top1.to_frame("abs_loading").to_html()))
        display(HTML("<h4>Top |loadings| for PC2</h4>" + top2.to_frame("abs_loading").to_html()))

        # Optional t-SNE (only if sample size reasonable)
        if _HAS_TSNE and Xs.shape[0] >= 200:
            tsne = TSNE(n_components=2, init="pca", learning_rate="auto", perplexity=min(30, max(5, Xs.shape[0]//50)), random_state=42)
            Zt = tsne.fit_transform(Xs)
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.scatter(Zt[:,0], Zt[:,1], s=8, alpha=0.7)
            ax2.set_title("t-SNE (2D)")
            plt.show()
    """)


def feature_selection(df):
    return dedent("""
        # ── Feature Selection (mutual info + permutation importance) ──────
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.inspection import permutation_importance
        from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
        from IPython.display import display, HTML
        try:
            from syntaxmatrix.display import show   # UI-safe
        except Exception:
            pass

        _df = df.copy()

        # ---- 1) Pick target y (heuristics; fall back gracefully)
        target_candidates = [
            "target", "label", "y", "outcome", "class", "response", "target_var"
        ]
        ycol = None
        for c in target_candidates:
            if c in _df.columns:
                ycol = c; break

        _reason = None
        if ycol is None:
            # 1a) Prefer a low-cardinality non-ID column (classification)
            low_card = []
            for c in _df.columns:
                try:
                    nun = _df[c].nunique(dropna=True)
                    if 2 <= nun <= 20 and str(c).lower() not in ("id","uuid","index"):
                        low_card.append(c)
                except Exception:
                    pass
            if low_card:
                ycol = low_card[-1]
                try:
                    show(f"Using provisional classification target: '{ycol}' (low-cardinality)", title="Feature Selection")
                except Exception:
                    pass

        if ycol is None:
            # 1b) Else take a high-variance numeric (regression)
            num = _df.select_dtypes(include=[np.number])
            if not num.empty:
                try:
                    ycol = num.var().sort_values(ascending=False).index[0]
                    _reason = "highest-variance numeric"
                    try:
                        show(f"Using provisional regression target: '{ycol}' ({_reason})", title="Feature Selection")
                    except Exception:
                        pass
                except Exception:
                    ycol = None

        _can_run = ycol is not None
        if not _can_run:
            # Friendly message and a proxy output so the block still yields value
            try:
                show("Feature selection needs a target. None detected and none could be inferred. Showing numeric variance as a proxy.", title="Feature Selection")
                var_df = _df.select_dtypes(include=[np.number]).var().sort_values(ascending=False).to_frame('variance').reset_index().rename(columns={'index':'feature'})
                show(var_df.head(15), title="Numeric variance (proxy)")
            except Exception:
                pass
        else:
            # ---- 2) Build X/y and simple preprocessing
            X = _df.drop(columns=[ycol]).copy()
            y = _df[ycol].copy()

            num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
            cat_cols = [c for c in X.columns if c not in num_cols]

            # Robust encoder across sklearn versions / environments
            try:
                enc = _SMX_OHE()
            except NameError:
                enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

            preproc = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(with_mean=True, with_std=True), num_cols) if num_cols else ("num","drop",[]),
                    ("cat", enc, cat_cols) if cat_cols else ("cat","drop",[]),
                ],
                remainder="drop",
                verbose_feature_names_out=False,
            )

            # classify vs regress
            y_is_classification = (y.nunique() <= 20) and (y.dtype.kind in "biuO" or y.nunique() <= 10)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.25, random_state=42, stratify=y if y_is_classification else None
            )

            if y_is_classification:
                base_est = LogisticRegression(max_iter=2000, n_jobs=None) if hasattr(LogisticRegression(), "n_jobs") else LogisticRegression(max_iter=2000)
                alt_est  = RandomForestClassifier(n_estimators=200, random_state=42)
                mi_func  = mutual_info_classif
                score_kw = {"scoring": "roc_auc"} if y.nunique()==2 else {"scoring": "balanced_accuracy"}
            else:
                try:
                    base_est = Ridge(random_state=42)
                except TypeError:
                    base_est = Ridge()
                alt_est  = RandomForestRegressor(n_estimators=200, random_state=42)
                mi_func  = mutual_info_regression
                score_kw = {"scoring": "r2"}

            pipe = Pipeline([("prep", preproc), ("est", base_est)])
            pipe.fit(X_train, y_train)

            # ---- 3) Mutual information (on one-hot expanded X)
            X_enc = pipe.named_steps["prep"].transform(X_train)
            # Get feature names after OHE
            try:
                ohe = pipe.named_steps["prep"].named_transformers_["cat"]
                if hasattr(ohe, 'get_feature_names_out'):
                    cat_feature_names = list(ohe.get_feature_names_out(cat_cols))
                else:
                    cat_feature_names = []
            except Exception:
                cat_feature_names = []
            feature_names = num_cols + cat_feature_names
            if len(feature_names) != (X_enc.shape[1] if hasattr(X_enc, 'shape') else len(feature_names)):
                # fallback if names length mismatch
                feature_names = [f"f{i}" for i in range(X_enc.shape[1])]

            # Mutual information scores
            try:
                mi = mi_func(y_train, X_enc) if callable(mi_func) else np.zeros(len(feature_names))
            except Exception:
                mi = np.zeros(len(feature_names))
            mi_df = pd.DataFrame({"feature": feature_names, "mi": mi}).sort_values("mi", ascending=False)

            # ---- 4) Permutation importance on alt estimator
            pipe_alt = Pipeline([("prep", preproc), ("est", alt_est)])
            pipe_alt.fit(X_train, y_train)
            try:
                pi = permutation_importance(pipe_alt, pipe_alt.named_steps["prep"].transform(X_test), y_test, n_repeats=5, random_state=42, **score_kw)
                pi_df = pd.DataFrame({"feature": feature_names, "perm_importance_mean": pi.importances_mean}).sort_values("perm_importance_mean", ascending=False)
            except Exception:
                pi_df = pd.DataFrame({"feature": feature_names, "perm_importance_mean": np.zeros(len(feature_names))})

            # ---- 5) Show results
            show(mi_df.head(20), title="Mutual information (top features)")
            show(pi_df.head(20), title="Permutation importance (top features)")

            # Horizontal bars for permutation importance
            top = pi_df.head(15)[::-1]
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(top["feature"], top["perm_importance_mean"])
            ax.set_title("Top permutation importances")
            ax.set_xlabel("Importance (mean over repeats)")
            plt.tight_layout(); plt.show()
    """)


def time_series_forecasting(df):
    return dedent("""
        # ── Auto-generated baseline time-series forecast ─────────
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_absolute_error
        
        _df = df.copy()

        # 1) pick a datetime column
        dt_cols = [c for c in _df.columns if np.issubdtype(_df[c].dtype, np.datetime64)]
        if not dt_cols:
            name_hits = [c for c in _df.columns if any(k in str(c).lower()
                            for k in ["date","time","timestamp","datetime","ds","period"])]
            for c in name_hits:
                try:
                    _df[c] = pd.to_datetime(_df[c], errors="raise")
                    dt_cols = [c]
                    break
                except Exception:
                    continue

        if not dt_cols:
            raise ValueError("No datetime-like column found for time-series forecasting.")

        time_col = dt_cols[0]

        # 2) pick a numeric target column
        num_cols = [c for c in _df.select_dtypes(include=['number', 'bool']).columns if c != time_col]
        if not num_cols:
            raise ValueError("No numeric target available for time-series forecasting.")

        target = num_cols[0]

        ts = _df[[time_col, target]].dropna().sort_values(time_col)
        ts["time_idx"] = (ts[time_col] - ts[time_col].min()).dt.total_seconds() / 86400.0

        if len(ts) < 10:
            raise ValueError("Not enough data points for time-series forecasting (need >= 10 rows).")

        split_idx = int(len(ts) * 0.8)
        train, test = ts.iloc[:split_idx], ts.iloc[split_idx:]

        X_train = train[["time_idx"]].values
        y_train = train[target].values
        X_test = test[["time_idx"]].values
        y_test = test[target].values

        reg = LinearRegression()
        reg.fit(X_train, y_train)

        y_pred = reg.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        show({{"MAE_forecast": mae}})

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(train[time_col], train[target], label="train")
        ax.plot(test[time_col], y_test, label="test")
        ax.plot(test[time_col], y_pred, label="forecast")
        ax.legend()
        ax.set_title(f"Baseline time-series forecast for {{target}}")
        plt.tight_layout()
        plt.show()
    """)


def time_series_classification(df, entity_col, time_col, target_col):
    return dedent(f"""
        # ── Auto-generated time-series classification baseline ─────
        import numpy as np
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, classification_report
        
        _df = df.copy()

        # Drop rows missing key columns
        _df = _df.dropna(subset=['{entity_col}', '{time_col}', '{target_col}'])

        # Ensure datetime for the time column
        _df['{time_col}'] = pd.to_datetime(_df['{time_col}'], errors="coerce")
        _df = _df.dropna(subset=['{time_col}'])

        # Sort by entity then time
        _df = _df.sort_values(['{entity_col}', '{time_col}'])

        # Numeric features only (excluding target, entity, time)
        num_cols = _df.select_dtypes(include=['number', 'bool']).columns.tolist()
        for c in ['{target_col}', '{entity_col}', '{time_col}']:
            if c in num_cols:
                num_cols.remove(c)

        if not num_cols:
            raise ValueError("No numeric features available for time-series classification template.")

        # Aggregate sequence into per-entity features
        agg_spec = {{}}
        for c in num_cols:
            agg_spec[c] = ['mean', 'std', 'min', 'max', 'last']

        grouped = _df.groupby('{entity_col}').agg(agg_spec)

        # Flatten MultiIndex columns
        grouped.columns = [f"{{col}}_{{stat}}" for col, stat in grouped.columns]

        # Target per entity: last observed label
        y = _df.groupby('{entity_col}')['{target_col}'].last()

        # Align X and y on the same entities
        X, y = grouped.align(y, join="inner", axis=0)

        if X.empty:
            raise ValueError("No aggregated rows available for time-series classification.")

        # Train/test split by entities
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        clf = RandomForestClassifier(n_estimators=300, random_state=42)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        show({{"Accuracy": acc}})

        report_df = pd.DataFrame(
            classification_report(y_test, y_pred, output_dict=True)
        ).T
        show(report_df)
    """)


def unknown_group_proxy_pack(df, group_col, unknown_tokens, numeric_cols, cat_cols, outcome_col=None):
    return dedent(f"""
        # ── Unknown Group: Proxy Insight Pack ──
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        
        _df = df.copy()

        if '{group_col}' not in _df.columns:
            show("Grouping column '{group_col}' not found; showing overall summary only.")
            show(_df.head())
        else:
            s = _df['{group_col}']
            s_norm = s.astype(str).str.strip().str.lower()
            _tokens = set({list({"unknown","not reported","not_reported","not known","n/a","na","none","nan","missing","unreported","unspecified","null","-",""})})
            _tokens.update({list(set(unknown_tokens))})
            is_unknown = s.isna() | s_norm.isin(_tokens)
            _df["_UnknownGroup"] = np.where(is_unknown, "Unknown/Not Reported", "Known")

            # 1) Size table (never errors)
            size_tbl = _df["_UnknownGroup"].value_counts(dropna=False).rename_axis("Group").reset_index(name="Count")
            total = len(_df) if len(_df) else 1
            size_tbl["Pct"] = (size_tbl["Count"] / total * 100).round(1)
            show(size_tbl)

        # 2) Numeric comparisons (auto-select; safe when empty)
        num_cols = [c for c in {list([])} or {list(set(numeric_cols))} if c in _df.columns and pd.api.types.is_numeric_dtype(_df[c])]
        if not num_cols:
            num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()[:6]

        if "_UnknownGroup" in _df.columns and num_cols:
            blocks = []
            for g, sub in _df.groupby("_UnknownGroup", dropna=False):
                if sub.empty:
                    continue
                desc = sub[num_cols].describe().T
                desc.insert(0, "Group", g)
                desc = desc.reset_index().rename(columns={{"index":"Variable","std":"Std","25%":"Q1","50%":"Median","75%":"Q3"}})
                blocks.append(desc[["Variable","Group","count","mean","Median","Std","min","Q1","Q3","max"]])
            numeric_summary = pd.concat(blocks, ignore_index=True) if blocks else pd.DataFrame(
                columns=["Variable","Group","count","mean","Median","Std","min","Q1","Q3","max"]
            )
            show(numeric_summary)

        # 3) Composition of categorical columns for Unknown group
        cat_cols = [c for c in {list(set(cat_cols))} if c in _df.columns]
        if "_UnknownGroup" in _df.columns and cat_cols:
            unk = _df[_df["_UnknownGroup"]=="Unknown/Not Reported"]
            comp_blocks = []
            if not unk.empty:
                for c in cat_cols:
                    vc = unk[c].astype(str).str.strip().replace({{"nan":"(missing)","":"(blank)"}}).value_counts(normalize=True, dropna=False)
                    comp = vc.mul(100).round(1).rename_axis("level").reset_index(name="Pct")
                    comp.insert(0, "Variable", c)
                    comp_blocks.append(comp)
            lifestyle_comp = pd.concat(comp_blocks, ignore_index=True) if comp_blocks else pd.DataFrame(columns=["Variable","level","Pct"])
            show(lifestyle_comp)

        # 4) Visuals — guarded; fall back silently if plotting fails
        try:
            if "_UnknownGroup" in _df.columns:
                ax = (size_tbl.set_index("Group")["Pct"]).plot(kind="bar", figsize=(5,3))
                ax.set_ylabel("% of records")
                ax.set_title(f"Known vs Unknown/Not Reported — {{'{group_col}'}}")
                plt.tight_layout(); plt.show()
        except Exception:
            pass

        # 5) Optional outcome prevalence
        if {repr(outcome_col)} and {repr(outcome_col)} in _df.columns and pd.api.types.is_numeric_dtype(_df[{repr(outcome_col)}]):
            try:
                prev = _df.groupby("_UnknownGroup")[{repr(outcome_col)}].mean() * 100.0
                show(prev.rename("Prevalence_%").reset_index())
            except Exception:
                pass

        # 6) Note on data capture
        note = (
            "Data capture: reduce 'Unknown/Not Reported' via intake prompts, pre-fill known values, "
            "audit repeated unknowns, and monitor Unknown rate over time and by site/channel."
        )
        show(note)
    """)


def viz_line(df, time_col=None, max_series=3, freq=None):
    """
    Plot up to `max_series` numeric columns against a detected datetime axis.
    - Detects a datetime/time-like column if `time_col` is None.
    - Optionally resamples to `freq` (e.g. 'D','W','M') if provided and evenly spaced lines are wanted.
    - Skips gracefully if no time or numeric columns are suitable.
    """
    return dedent(f"""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        
        _df = df.copy()

        # 1) choose time column
        time_col = {repr(time_col)}  # may be None
        if time_col is None:
            dt_cols = [c for c in _df.columns if np.issubdtype(_df[c].dtype, np.datetime64)]
            if not dt_cols:
                # name hints as fallback
                keys = ["date","time","timestamp","datetime","ds","period"]
                for c in _df.columns:
                    n = str(c).lower()
                    if any(k in n for k in keys):
                        try:
                            _df[c] = pd.to_datetime(_df[c], errors="coerce")
                            if _df[c].notna().any():
                                dt_cols = [c]
                                break
                        except Exception:
                            pass
            time_col = dt_cols[0] if dt_cols else None

        if not time_col or time_col not in _df.columns:
            show("⚠ No datetime-like column detected for a line chart; skipping.")
        else:
            _df = _df.dropna(subset=[time_col]).sort_values(time_col)
            # 2) pick up to `max_series` numeric columns (by variance)
            num_cols = [c for c in _df.select_dtypes(include=['number','bool']).columns if c != time_col]
            scored = []
            for c in num_cols:
                v = _df[c].dropna()
                scored.append((float(v.var()) if len(v) else 0.0, c))
            scored.sort(reverse=True)
            keep = [c for _, c in scored[:{max_series}]]

            if not keep:
                show("⚠ No numeric columns available for a line chart; skipping.")
            else:
                plot_df = _df[[time_col] + keep].copy()
                # optional resample
                if {repr(freq)} and plot_df[time_col].notna().any():
                    plot_df = plot_df.set_index(time_col).resample({repr(freq)}).mean().reset_index()

                fig, ax = plt.subplots(figsize=(8, 4))
                for c in keep:
                    ax.plot(plot_df[time_col], plot_df[c], label=str(c))
                ax.set_xlabel(str(time_col))
                ax.set_ylabel("Value")
                ax.legend(loc="best", frameon=False)
                ax.set_title("Line chart")
                plt.tight_layout()
                plt.show()
    """)


def clustering(df):
    return dedent("""
        # ==== CLUSTERING BASELINE (KMeans + DBSCAN fallback) ====
        import numpy as np, pandas as pd
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans, DBSCAN
        from sklearn.metrics import silhouette_score
        from sklearn.decomposition import PCA
        import matplotlib.pyplot as plt
        
        _work = df.copy()
        num_cols = _work.select_dtypes(include=[np.number]).columns.tolist()

        if len(num_cols) < 2:
            show(f"Clustering needs at least two numeric columns. Found: {num_cols}")
        else:
            X = _work[num_cols]
            pipe = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])
            Xp = pipe.fit_transform(X)

            n = Xp.shape[0]
            k_max = max(2, min(12, n - 1))
            best_k, best_sil = None, -1
            inertias, ks = [], []

            for k in range(2, k_max + 1):
                km = KMeans(n_clusters=k, n_init="auto", random_state=42)
                labels_k = km.fit_predict(Xp)
                if len(set(labels_k)) < 2:
                    continue
                sil = silhouette_score(Xp, labels_k)
                inertias.append(km.inertia_); ks.append(k)
                if sil > best_sil:
                    best_sil, best_k = sil, k

            model_label = "KMeans"
            if best_k is not None:
                model = KMeans(n_clusters=best_k, n_init="auto", random_state=42).fit(Xp)
                labels = model.labels_
                show({"model": model_label, "k": best_k, "silhouette": round(best_sil, 3)})
            else:
                model = DBSCAN(eps=0.8, min_samples=10).fit(Xp)
                labels = model.labels_
                model_label = "DBSCAN"
                show({"model": model_label})

            _work["cluster"] = labels
            show(_work["cluster"].value_counts().sort_index().rename("count").to_frame())

            prof = _work.groupby("cluster")[num_cols].agg(["mean","median","std","min","max","count"])
            show(prof)

            pca = PCA(n_components=2, random_state=42)
            comps = pca.fit_transform(Xp)
            fig, ax = plt.subplots(figsize=(7,5))
            for cl in sorted(set(labels)):
                mask = labels == cl
                ax.scatter(comps[mask,0], comps[mask,1], s=20, alpha=0.7, label=f"cluster {cl}")
            ax.set_title("PCA scatter of clusters"); ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
            ax.legend(loc="best"); plt.tight_layout(); plt.show()

            if ks:
                fig2, ax2 = plt.subplots(figsize=(7,4))
                ax2.plot(ks, inertias, marker="o")
                ax2.set_title("KMeans inertia by k"); ax2.set_xlabel("k"); ax2.set_ylabel("Inertia (SSE)")
                plt.tight_layout(); plt.show()

            df[:] = _work
    """)


def recommendation(df):
    return dedent("""
        # ==== ITEM-ITEM RECOMMENDATION (Nearest Neighbours over mixed features) ====
        import numpy as np, pandas as pd
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.neighbors import NearestNeighbors

        _work = df.copy()

        # --- 1) Identify features (numeric + categorical) ---
        num_cols = _work.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = _work.select_dtypes(include=["object", "category", "string"]).columns.tolist()

        # Heuristic: drop obvious IDs from features
        id_like = [c for c in _work.columns if (c.lower() in ("id","uid","uuid","record_id","row_id") or c.lower().endswith("_id"))]
        num_cols = [c for c in num_cols if c not in id_like]
        cat_cols = [c for c in cat_cols if c not in id_like]

        # Minimal guard
        if len(num_cols) + len(cat_cols) < 1:
            show("No usable feature columns for recommendation.");  # caption comes from PREFACE
        else:
            # --- 2) Build preprocessing (robust across sklearn versions) ---
            try:
                enc = _SMX_OHE()
            except NameError:
                # Fallback if PREFACE wasn't injected for some reason
                enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

            pre = ColumnTransformer(
                transformers=[
                    ("num", Pipeline([("scaler", StandardScaler())]), num_cols) if num_cols else ("num", "drop", []),
                    ("cat", enc, cat_cols) if cat_cols else ("cat", "drop", []),
                ],
                remainder="drop"
            )

            # --- 3) Sample cap for safety on huge tables ---
            N = len(_work)
            cap = min(N, 5000)
            _sample = _work.sample(n=cap, random_state=42) if N > cap else _work

            X = pre.fit_transform(_sample)
            if getattr(X, "shape", (0,0))[0] < 2:
                show("Not enough rows to compute neighbours.")
            else:
                # --- 4) Fit cosine NN and pick a few anchors ---
                k = min(6, X.shape[0])  # includes self; we'll drop it
                nn = NearestNeighbors(metric="cosine", n_neighbors=k)
                nn.fit(X)

                # Anchor strategy: prefer rows with an id-like column; otherwise first few
                anchor_ids = None
                if id_like:
                    anchor_ids = _sample[id_like[0]].head(min(5, len(_sample))).tolist()
                    anchors = _sample.index[:len(anchor_ids)].tolist()
                else:
                    anchors = _sample.index[:min(5, len(_sample))].tolist()

                # For readability, pick up to 4 descriptive (non-numeric) columns
                desc_cols = [c for c in _sample.columns if c in cat_cols][:4]
                meta_cols = (id_like[:1] + desc_cols)[:5]

                # --- 5) Build neighbour tables per anchor ---
                for pos, aidx in enumerate(anchors):
                    # position of aidx inside _sample
                    loc = list(_sample.index).index(aidx)
                    dists, inds = nn.kneighbors(X[loc].reshape(1, -1), return_distance=True)
                    dists, inds = dists[0].tolist(), inds[0].tolist()

                    rows = []
                    for dist, i in zip(dists, inds):
                        if i == loc:
                            continue  # drop self
                        ridx = _sample.index[i]
                        row = {"rank": len(rows)+1, "distance": float(dist), "_index": int(ridx)}
                        for c in meta_cols:
                            if c in _sample.columns:
                                row[c] = _sample.loc[ridx, c]
                        rows.append(row)

                    out = pd.DataFrame(rows)
                    title = "Similar items" if not id_like else f"Similar to {id_like[0]}={_sample.loc[aidx, id_like[0]]}"
                    show(out, title=title)

                # Summary
                feats = len(num_cols) + len(cat_cols)
                show({"rows_used": X.shape[0], "features": feats}, title="Recommendation set-up summary")
    """)


def topic_modelling(df):

    return dedent("""
        # ==== TOPIC MODELLING (LDA with safe fallback) ====
        import numpy as np, pandas as pd, re
        import matplotlib.pyplot as plt

        # --- 1) Pick a text column (or compose one) ---
        _df = df.copy()
        text_cols_named = [c for c in _df.columns if any(k in c.lower() for k in ["text","review","description","comment","notes","content","body","message","title"])]
        obj_cols = _df.select_dtypes(include=["object","string"]).columns.tolist()
        candidates = text_cols_named + [c for c in obj_cols if c not in text_cols_named]

        def _choose_text_col(d):
            best, best_score = None, -1
            for c in candidates or []:
                s = d[c].astype(str).fillna("")
                # token score: average length and alphabetic ratio
                tokens = s.str.split()
                score = float(tokens.map(len).mean() or 0) + float((s.str.contains(r"[A-Za-z]", regex=True)).mean()) * 2.0
                if score > best_score:
                    best, best_score = c, score
            return best

        text_col = _choose_text_col(_df)
        if text_col is None:
            # build a composite text if nothing obvious
            parts = obj_cols[:4]
            if not parts:
                show("No suitable text columns found for topic modelling.")
            else:
                _df["_smx_text"] = _df[parts].astype(str).agg(" ".join, axis=1)
                text_col = "_smx_text"

        if text_col is not None:
            docs = _df[text_col].astype(str).fillna("").tolist()
            n_docs = len(docs)

            # --- 2) Choose topic count sensibly ---
            n_topics = int(np.clip(max(3, int(np.sqrt(max(1, n_docs/50)))) , 3, 12))

            # --- 3) Try LDA; if it fails, fall back to n-gram frequencies ---
            used_lda = False
            try:
                from sklearn.feature_extraction.text import CountVectorizer
                from sklearn.decomposition import LatentDirichletAllocation
                vect = CountVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))
                X = vect.fit_transform(docs)
                if X.shape[0] < 5 or X.shape[1] < 10:
                    raise RuntimeError("Too little text to fit LDA.")
                lda = LatentDirichletAllocation(n_components=n_topics, learning_method="batch", random_state=42)
                W = lda.fit_transform(X)            # doc-topic
                H = lda.components_                 # topic-term
                terms = np.array(vect.get_feature_names_out())

                # --- topic → top words table ---
                rows = []
                for k in range(n_topics):
                    inds = np.argsort(H[k])[::-1][:12]
                    words = terms[inds]
                    weights = H[k, inds]
                    rows.append({"topic": k, "top_terms": ", ".join(words[:10])})
                top_words = pd.DataFrame(rows)
                show(top_words, title="Topics and top terms")

                # --- doc dominant topic + prevalence ---
                dom = W.argmax(axis=1)
                strength = W.max(axis=1)
                _df["topic"] = dom
                _df["topic_score"] = strength
                # prevalence plot
                prev = pd.Series(dom).value_counts().sort_index()
                fig, ax = plt.subplots(figsize=(7,4))
                prev.plot(kind="bar", ax=ax)
                ax.set_title("Topic prevalence"); ax.set_xlabel("topic"); ax.set_ylabel("documents")
                plt.tight_layout(); plt.show()

                show(_df[["topic","topic_score"]].head(20), title="Document-topic sample")
                used_lda = True

            except Exception as e:
                # --- Fallback: simple n-gram frequency table ---
                try:
                    from sklearn.feature_extraction.text import CountVectorizer
                    vect = CountVectorizer(stop_words="english", max_features=3000, ngram_range=(1,2))
                    X = vect.fit_transform(docs)
                    counts = np.asarray(X.sum(axis=0)).ravel()
                    terms = np.array(vect.get_feature_names_out())
                    top = pd.DataFrame({"term": terms, "count": counts}).sort_values("count", ascending=False).head(30)
                    show(top, title="Top terms (fallback)")
                except Exception:
                    show("Text vectorisation unavailable; cannot compute topics.")
                used_lda = False

            # Summary
            show({"docs": n_docs, "topics": (n_topics if used_lda else 0)}, title="Topic modelling summary")
    """)


def viz_pie(df, category_col=None, top_k=8):
    """Generic pie chart of category shares."""
    return dedent("""
        import pandas as pd
        import matplotlib.pyplot as plt
        from syntaxmatrix.display import show

        _df = df.copy()

        # auto pick categorical column if not provided
        cat = __SMX_CAT_HINT__
        if cat is None or cat not in _df.columns:
            cat_cols = [c for c in _df.columns
                        if (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category'))
                        and _df[c].nunique(dropna=True) > 1]
            if not cat_cols:
                raise ValueError("No suitable categorical column for pie chart.")
            cat = cat_cols[0]

        s = _df[cat].astype(str).fillna("Missing").value_counts()
        if len(s) > __SMX_TOPK__:
            s = pd.concat([s.iloc[:__SMX_TOPK__], pd.Series({"Other": s.iloc[__SMX_TOPK__:].sum()})])

        pie_df = s.reset_index()
        pie_df.columns = [cat, "count"]
        pie_df["percent"] = (pie_df["count"] / pie_df["count"].sum() * 100).round(2)
        show(pie_df)

        plt.figure(figsize=(5,5))
        plt.pie(pie_df["count"], labels=pie_df[cat], autopct='%1.1f%%', startangle=90)
        plt.title(f"Composition of {cat}")
        plt.tight_layout()
        plt.show()
    """.replace("__SMX_CAT_HINT__", repr(category_col))
       .replace("__SMX_TOPK__", str(top_k)))


def viz_violin(df, x=None, y=None, hue=None, sample_n=2000):
    """Violin plot for numeric distribution across categories."""
    return dedent("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from syntaxmatrix.display import show

        _df = df.copy()

        xcol = __SMX_X__
        ycol = __SMX_Y__
        hcol = __SMX_HUE__

        if xcol is None or xcol not in _df.columns:
            cat_cols = [c for c in _df.columns
                        if (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category'))
                        and _df[c].nunique(dropna=True) > 1
                        and _df[c].nunique(dropna=True) <= 20]
            xcol = cat_cols[0] if cat_cols else None

        if ycol is None or ycol not in _df.columns:
            num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
            ycol = num_cols[0] if num_cols else None

        if xcol is None or ycol is None:
            raise ValueError("Need one categorical (x) and one numeric (y) column for violin plot.")

        use_cols = [xcol, ycol]
        if hcol in _df.columns and hcol not in (xcol, ycol):
            use_cols.append(hcol)

        _work = _df[use_cols].dropna()
        if len(_work) > __SMX_SAMPLE_N__:
            _work = _work.sample(__SMX_SAMPLE_N__, random_state=42)

        # Use seaborn if available, else fallback to boxplot
        try:
            import seaborn as sns
            plt.figure(figsize=(7,4))
            sns.violinplot(
                data=_work,
                x=xcol, y=ycol,
                hue=hcol if hcol in _work.columns else None,
                cut=0
            )
            plt.title(f"{ycol} distribution by {xcol}")
            plt.tight_layout()
            plt.show()
        except Exception:
            plt.figure(figsize=(7,4))
            _work.boxplot(column=ycol, by=xcol, grid=False)
            plt.title(f"{ycol} by {xcol} (box fallback)")
            plt.suptitle("")
            plt.tight_layout()
            plt.show()

        show(_work.groupby(xcol)[ycol].describe().round(2))
    """.replace("__SMX_X__", repr(x))
       .replace("__SMX_Y__", repr(y))
       .replace("__SMX_HUE__", repr(hue))
       .replace("__SMX_SAMPLE_N__", str(sample_n)))


def viz_stacked_bar(df, x=None, hue=None, normalise=True, top_k=8):
    """Stacked (optionally % stacked) bar chart for two categoricals."""
    return dedent("""
        import pandas as pd
        import matplotlib.pyplot as plt
        from syntaxmatrix.display import show

        _df = df.copy()

        xcol = __SMX_X__
        hcol = __SMX_HUE__

        cat_cols = [c for c in _df.columns
                    if (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category'))
                    and _df[c].nunique(dropna=True) > 1
                    and _df[c].nunique(dropna=True) <= 30]

        if xcol is None or xcol not in _df.columns:
            xcol = cat_cols[0] if cat_cols else None
        if hcol is None or hcol not in _df.columns:
            hcol = cat_cols[1] if len(cat_cols) > 1 else None

        if xcol is None or hcol is None:
            raise ValueError("Need two categorical columns for stacked bar chart.")

        _work = _df[[xcol, hcol]].dropna()

        keep_h = _work[hcol].astype(str).value_counts().index[:__SMX_TOPK__]
        _work[hcol] = _work[hcol].astype(str).where(_work[hcol].astype(str).isin(keep_h), other="Other")

        tab = pd.crosstab(_work[xcol].astype(str), _work[hcol].astype(str))
        show(tab)

        plot_tab = tab.copy()
        if __SMX_NORM__:
            plot_tab = plot_tab.div(plot_tab.sum(axis=1), axis=0) * 100

        ax = plot_tab.plot(kind="bar", stacked=True, figsize=(8,4))
        ax.set_title(
            f"{hcol} composition by {xcol}" + (" (%)" if __SMX_NORM__ else "")
        )
        ax.set_xlabel(xcol)
        ax.set_ylabel("Percent" if __SMX_NORM__ else "Count")
        plt.legend(title=hcol, bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        plt.show()
    """.replace("__SMX_X__", repr(x))
       .replace("__SMX_HUE__", repr(hue))
       .replace("__SMX_NORM__", "True" if normalise else "False")
       .replace("__SMX_TOPK__", str(top_k)))


def viz_distribution(df, col=None, by=None, bins=30, sample_n=5000):
    """Histogram distribution for a numeric column, optionally split by a category."""
    return dedent("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from syntaxmatrix.display import show

        _df = df.copy()
        ncol = __SMX_COL__
        bcol = __SMX_BY__

        if ncol is None or ncol not in _df.columns:
            num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
            ncol = num_cols[0] if num_cols else None

        if ncol is None:
            raise ValueError("No numeric column available for distribution plot.")

        if bcol is not None and bcol not in _df.columns:
            bcol = None

        use_cols = [ncol] + ([bcol] if bcol else [])
        _work = _df[use_cols].dropna()

        if len(_work) > __SMX_SAMPLE_N__:
            _work = _work.sample(__SMX_SAMPLE_N__, random_state=42)

        plt.figure(figsize=(7,4))
        if bcol:
            try:
                import seaborn as sns
                sns.histplot(
                    data=_work, x=ncol, hue=bcol,
                    bins=__SMX_BINS__,
                    stat="density",
                    common_norm=False,
                    element="step"
                )
            except Exception:
                for k, g in _work.groupby(bcol):
                    plt.hist(g[ncol], bins=__SMX_BINS__, alpha=0.5, density=True, label=str(k))
                plt.legend(title=bcol)
        else:
            plt.hist(_work[ncol], bins=__SMX_BINS__, alpha=0.8)

        plt.title(f"Distribution of {ncol}" + (f" by {bcol}" if bcol else ""))
        plt.xlabel(ncol)
        plt.ylabel("Density" if bcol else "Count")
        plt.tight_layout()
        plt.show()

        show(_work[ncol].describe().round(2))
    """.replace("__SMX_COL__", repr(col))
       .replace("__SMX_BY__", repr(by))
       .replace("__SMX_BINS__", str(bins))
       .replace("__SMX_SAMPLE_N__", str(sample_n)))


def viz_area(df, x=None, y=None, group=None, sample_n=3000):
    # richer time/area plot (useful for trends)
    return dedent(f"""
    import matplotlib.pyplot as plt
    from syntaxmatrix.display import show

    _df = df.copy()

    # auto-pick numeric columns
    num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
    cat_cols = [c for c in _df.columns if c not in num_cols and _df[c].nunique(dropna=True) <= 12]

    if x is None or x not in _df.columns:
        x = None  # area plot can be index-based
    if y is None or y not in _df.columns:
        y = num_cols[0] if num_cols else None
    if group is None or group not in _df.columns:
        group = cat_cols[0] if cat_cols else None

    if y is None:
        show("⚠ No numeric column for area plot.")
    else:
        dplot = _df[[c for c in [x,y,group] if c]].dropna()
        if len(dplot) > sample_n:
            dplot = dplot.sample(sample_n, random_state=42)

        if x:
            dplot = dplot.sort_values(x)

        plt.figure(figsize=(7,3.5))
        if group is None:
            plt.fill_between(range(len(dplot)), dplot[y].values, alpha=0.6)
            plt.title(f"Area plot of {y}")
        else:
            for k, g in dplot.groupby(group):
                plt.fill_between(range(len(g)), g[y].values, alpha=0.4, label=str(k))
            plt.legend()
            plt.title(f"{y} area plot by {group}")
        plt.tight_layout()
        plt.show()
    """)


def viz_kde(df, col=None, by=None, sample_n=5000):
    return dedent(f"""
    import matplotlib.pyplot as plt
    from syntaxmatrix.display import show

    _df = df.copy()
    num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
    cat_cols = [c for c in _df.columns if c not in num_cols and _df[c].nunique(dropna=True) <= 12]

    if col is None or col not in _df.columns:
        col = num_cols[0] if num_cols else None
    if by is None or by not in _df.columns:
        by = cat_cols[0] if cat_cols else None

    if col is None:
        show("⚠ No numeric column for density plot.")
    else:
        dplot = _df[[c for c in [col,by] if c]].dropna()
        if len(dplot) > sample_n:
            dplot = dplot.sample(sample_n, random_state=42)

        plt.figure(figsize=(6,3.5))
        try:
            if by is None:
                sns.kdeplot(data=dplot, x=col, fill=True)
                plt.title(f"Density of {col}")
            else:
                sns.kdeplot(data=dplot, x=col, hue=by, fill=True, common_norm=False)
                plt.title(f"Density of {col} by {by}")
        except Exception:
            # matplotlib fallback
            if by is None:
                dplot[col].plot(kind="kde")
            else:
                for k, g in dplot.groupby(by):
                    g[col].plot(kind="kde", label=str(k))
                plt.legend()
        plt.tight_layout()
        plt.show()
    """)


def viz_count_bar(df, category_col=None, top_k=12):
    return dedent("""
    import matplotlib.pyplot as plt
    from syntaxmatrix.display import show

    _df = df.copy()

    # Auto-pick a sensible categorical column if none provided
    if category_col is None or category_col not in _df.columns:
        num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
        cat_cols = [
            c for c in _df.columns
            if c not in num_cols
            and (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category') or _df[c].nunique(dropna=True) <= 25)
        ]
        # Prefer low-cardinality cols
        cat_cols = [c for c in cat_cols if 2 <= _df[c].nunique(dropna=True) <= 25]
        category_col = cat_cols[0] if cat_cols else None

    if category_col is None:
        show("⚠ No categorical column available for count bar chart.")
    else:
        s = _df[category_col].astype(str)
        vc = s.value_counts()

        # Trim long tails so the bar stays readable
        if len(vc) > top_k:
            head = vc.head(top_k)
            tail_sum = vc.iloc[top_k:].sum()
            vc = head.copy()
            if tail_sum > 0:
                vc.loc["Other"] = tail_sum

        plt.figure(figsize=(7, 3.8))
        plt.bar(vc.index.astype(str), vc.values)
        plt.xticks(rotation=0, ha="center")
        plt.title(f"Counts by {category_col}")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

        show(vc.rename("count").reset_index().rename(columns={"index": category_col}))
    """)


from textwrap import dedent

def viz_scatter(df, x=None, y=None, hue=None, sample_n=2000):
    return dedent("""
    import matplotlib.pyplot as plt
    from syntaxmatrix.display import show

    _df = df.copy()

    num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
    cat_cols = [
        c for c in _df.columns
        if c not in num_cols
        and (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category') or _df[c].nunique(dropna=True) <= 20)
    ]
    cat_cols = [c for c in cat_cols if 2 <= _df[c].nunique(dropna=True) <= 20]

    if x is None or x not in _df.columns:
        x = num_cols[0] if len(num_cols) > 0 else None
    if y is None or y not in _df.columns:
        y = num_cols[1] if len(num_cols) > 1 else None
    if hue is None or hue not in _df.columns:
        hue = cat_cols[0] if cat_cols else None

    if x is None or y is None:
        show("⚠ Not enough numeric columns for scatter plot.")
    else:
        cols = [c for c in [x, y, hue] if c is not None]
        dplot = _df[cols].dropna()

        if len(dplot) > sample_n:
            dplot = dplot.sample(sample_n, random_state=42)

        plt.figure(figsize=(6, 4))
        if hue is None:
            plt.scatter(dplot[x], dplot[y], alpha=0.6)
            plt.title(f"{y} vs {x}")
            plt.xlabel(x); plt.ylabel(y)
        else:
            try:
                ax = sns.scatterplot(data=dplot, x=x, y=y, hue=hue)
                ax.set_title(f"{y} vs {x} by {hue}")
            except Exception:
                for k, g in dplot.groupby(hue):
                    plt.scatter(g[x], g[y], label=str(k), alpha=0.6)
                plt.legend()
                plt.title(f"{y} vs {x} by {hue}")
                plt.xlabel(x); plt.ylabel(y)

        plt.tight_layout()
        plt.show()
    """)


def viz_box(df, x=None, y=None, sample_n=3000):
    return dedent("""
    import matplotlib.pyplot as plt
    from syntaxmatrix.display import show

    _df = df.copy()

    # Identify numeric and categorical candidates
    num_cols = _df.select_dtypes(include=['number','bool']).columns.tolist()
    cat_cols = [
        c for c in _df.columns
        if c not in num_cols
        and (_df[c].dtype == 'object' or str(_df[c].dtype).startswith('category') or _df[c].nunique(dropna=True) <= 25)
    ]
    cat_cols = [c for c in cat_cols if 2 <= _df[c].nunique(dropna=True) <= 25]

    # Auto-pick y (numeric) and x (categorical) if not provided
    if y is None or y not in _df.columns:
        y = num_cols[0] if num_cols else None
    if x is None or x not in _df.columns:
        x = cat_cols[0] if cat_cols else None

    if y is None:
        show("⚠ No numeric column available for box plot.")
    else:
        cols = [c for c in [x, y] if c is not None]
        dplot = _df[cols].dropna()

        if len(dplot) > sample_n:
            dplot = dplot.sample(sample_n, random_state=42)

        if x is None:
            plt.figure(figsize=(5.5, 3.8))
            plt.boxplot(dplot[y])
            plt.title(f"Distribution of {y}")
            plt.ylabel(y)
        else:
            # seaborn if available, else matplotlib grouped box
            try:
                ax = sns.boxplot(data=dplot, x=x, y=y)
                ax.set_title(f"{y} by {x}")
                ax.set_xlabel(x); ax.set_ylabel(y)
            except Exception:
                groups = [g[y].values for _, g in dplot.groupby(x)]
                labels = [str(k) for k in dplot.groupby(x).groups.keys()]
                plt.figure(figsize=(7.5, 3.8))
                plt.boxplot(groups, labels=labels)
                plt.title(f"{y} by {x}")
                plt.xlabel(x); plt.ylabel(y)

        plt.tight_layout()
        plt.show()

        # Show a quick summary table too
        if x is None:
            show(dplot[y].describe())
        else:
            show(dplot.groupby(x)[y].describe())
    """)