# syntaxmatrix/dataset_preprocessing.py
# -----------------------------------------------------------------------------
# Dataset-agnostic cleaning for analysis with imputation and audit outputs.
# Writes:
#   DATA_FOLDER / selected_dataset / cleaned_df.csv
#   DATA_FOLDER / selected_dataset / missingness.csv
# Does NOT mutate the in-memory EDA df. Call ensure_cleaned_df(...) after df load.
# -----------------------------------------------------------------------------

from __future__ import annotations
import os
import re
import pandas as pd
import numpy as np
from typing import Tuple, Dict

__all__ = ["ensure_cleaned_df"]

# Common tokens that should be treated as missing
_MISSING_TOKENS = {
    "", "na", "n/a", "n.a.", "nan", "none", "null", "-", "--", "?", "unknown"
}

_BOOL_TRUE  = {"true", "t", "yes", "y", "1", "on"}
_BOOL_FALSE = {"false", "f", "no", "n", "0", "off"}

# Columns whose names hint at date/time content (case-insensitive)
_DATE_HINTS = re.compile(r"(date|time|timestamp|_dt)$", re.IGNORECASE)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _strip_column_names_only(df: pd.DataFrame) -> pd.DataFrame:
    """Trim surrounding whitespace in column names (preserve original names)."""
    df = df.copy()
    df.rename(columns=lambda c: str(c).strip(), inplace=True)
    return df

def _standardise_missing_tokens(s: pd.Series) -> pd.Series:
    """Map common missing tokens to NaN in object-like columns."""
    if s.dtype != "object":
        return s
    mapped = s.astype(str).str.strip()
    lowered = mapped.str.lower()
    is_missing = lowered.isin(_MISSING_TOKENS)
    mapped = mapped.mask(is_missing, np.nan)
    return mapped

def _coerce_booleans(s: pd.Series) -> pd.Series:
    if s.dtype != "object":
        return s
    cand = s.astype(str).str.strip().str.lower()
    uniq = set(cand.dropna().unique().tolist())
    if uniq and uniq.issubset(_BOOL_TRUE | _BOOL_FALSE):
        return cand.map(lambda v: True if v in _BOOL_TRUE else False if v in _BOOL_FALSE else np.nan)
    return s

_NUM_RE = re.compile(r"[,\s£$€]")

def _looks_numeric(x: str) -> bool:
    v = _NUM_RE.sub("", x.strip()).replace("%", "")
    return bool(re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)$", v))

def _coerce_numerics(s: pd.Series) -> pd.Series:
    if s.dtype != "object":
        return s
    sample = s.dropna().astype(str).head(1000)
    if len(sample) == 0:
        return s
    ratio = np.mean([_looks_numeric(x) for x in sample])
    if ratio >= 0.8:
        cleaned = _NUM_RE.sub("", s.astype(str).str.strip())
        # If many values end with %, interpret as percent
        if (cleaned.str.endswith("%")).mean() > 0.6:
            # remove % and divide by 100
            cleaned = cleaned.str.replace("%", "", regex=False)
            out = pd.to_numeric(cleaned, errors="coerce") / 100.0
        else:
            out = pd.to_numeric(cleaned.str.replace("%", "", regex=False), errors="coerce")
        return out
    return s

def _parse_datetimes(df: pd.DataFrame, col: str) -> pd.Series:
    """Parse datetimes robustly; produce tz-naive UTC for consistent .dt."""
    s = df[col].astype(str)
    dt = pd.to_datetime(s, errors="coerce", infer_datetime_format=True, utc=True)
    if dt.isna().mean() > 0.9:
        # strip trailing ' (PDT)' etc.
        s2 = s.str.replace(r"\s*\([^)]*\)\s*$", "", regex=True)
        dt = pd.to_datetime(s2, errors="coerce", infer_datetime_format=True, utc=True)
    # Convert to tz-naive UTC if we parsed anything meaningful
    if dt.notna().sum() >= max(3, int(0.1 * len(df))):
        try:
            return dt.dt.tz_convert("UTC").dt.tz_localize(None)
        except Exception:
            return dt  # already tz-naive
    return df[col]  # leave original if parsing failed

def _summarise_missingness(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    miss = df.isna().sum()
    pct = (miss / total * 100.0).round(2)
    dtype = df.dtypes.astype(str)
    return pd.DataFrame({"column": df.columns, "missing": miss.values, "missing_%": pct.values, "dtype": dtype.values})

# -----------------------------------------------------------------------------
# Main cleaner (type coercion + imputation for analysis)
# -----------------------------------------------------------------------------

def _clean_and_coerce(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 0) tidy strings and standardise missing tokens
    for c in df.columns:
        s = df[c]
        if s.dtype == "object":
            s = s.astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
            s = _standardise_missing_tokens(s)
            df[c] = s

    # 1) booleans
    for c in df.columns:
        df[c] = _coerce_booleans(df[c])

    # 2) numerics
    for c in df.columns:
        df[c] = _coerce_numerics(df[c])

    # 3) datetimes (by name hint + explicit 'saledate')
    for c in list(df.columns):
        n = str(c).lower()
        if _DATE_HINTS.search(n) or n == "saledate":
            try:
                df[c] = _parse_datetimes(df, c)
            except Exception:
                pass

    # 4) drop exact duplicates
    df = df.drop_duplicates()
    return df

def _impute_for_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Impute missing values:
      - numeric -> median
      - categorical/object/bool -> most frequent (fallback 'Unknown')
    Adds <col>__imputed boolean flags where any fills occurred.
    Returns cleaned df and a dict of imputation strategies used.
    """
    df = df.copy()
    strategy: Dict[str, str] = {}

    # numeric
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    for c in num_cols:
        if df[c].isna().any():
            med = df[c].median(skipna=True)
            if pd.isna(med):
                continue  # cannot impute an all-NaN column
            df[f"{c}__imputed"] = df[c].isna()
            df[c] = df[c].fillna(med)
            strategy[c] = "median"

    # categoricals & booleans (object/category/bool)
    cat_cols = [c for c in df.columns
                if df[c].dtype == "object" or str(df[c].dtype).startswith("category") or df[c].dtype == "bool"]
    for c in cat_cols:
        if df[c].isna().any():
            # mode; if multiple modes, pick the first stable value
            try:
                mode_val = df[c].mode(dropna=True)
                fill = mode_val.iloc[0] if not mode_val.empty else "Unknown"
            except Exception:
                fill = "Unknown"
            df[f"{c}__imputed"] = df[c].isna()
            df[c] = df[c].fillna(fill)
            strategy[c] = f"mode('{fill}')"

    return df, strategy

def ensure_cleaned_df(DATA_FOLDER: str, cleaned_folder: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Build (or reuse) an analysis-ready cleaned dataset and persist to:
        f"{DATA_FOLDER}/{selected_dataset}/cleaned_df.csv"
    Also writes a missingness audit:
        f"{DATA_FOLDER}/{selected_dataset}/missingness.csv"
    Returns the cleaned frame. Does NOT mutate the provided df.
    """
    target_dir = os.path.join(DATA_FOLDER, cleaned_folder)
    os.makedirs(target_dir, exist_ok=True)
    target_csv = os.path.join(target_dir, "cleaned_df.csv")
    # miss_csv   = os.path.join(target_dir, "missingness.csv")
    

    # If a cleaned file already exists, reuse it (your pipeline already calls this once per dataset)
    if os.path.exists(target_csv):
        try:
            return pd.read_csv(target_csv, low_memory=False)
        except Exception:
            # fall through to rebuild if unreadable
            pass

    # Pipeline: normalise headers → coerce types → impute → audits → save
    step0 = _strip_column_names_only(df)
    step1 = _clean_and_coerce(step0)
    # audit BEFORE imputation (raw missingness after coercion)
    #_summarise_missingness(step1).to_csv(miss_csv, index=False)
    step2, _strategy = _impute_for_analysis(step1)

    # Drop id-like columns (high-uniqueness or name pattern)
    name_hit = [c for c in step2.columns if re.search(r'\b(id|uuid|vin|serial|record|row_?id)\b', c, re.I)]
    uniq_hit = [c for c in step2.columns if step2[c].nunique(dropna=True) >= 0.98 * len(step2)]
    id_like = sorted(set(name_hit) | set(uniq_hit))
    step2 = step2.drop(columns=id_like, errors='ignore')

    # Persist cleaned for tasks
    step2.to_csv(target_csv, index=False)
    return step2
