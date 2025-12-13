# syntaxmatrix/project_root.py 
import os
import inspect
from pathlib import Path
import syntaxmatrix

def scandir() -> Path:
    framework_dir = Path(syntaxmatrix.__file__).resolve().parent
    for frame in inspect.stack():
        fname = frame.filename
        if not fname or not isinstance(fname, str):
            continue
        p = Path(fname)
        try:
            if p.is_file() and framework_dir not in p.parents:
                return p.parent
        except Exception:
            continue
    return framework_dir

def _writable(p: Path) -> bool:
    try:
        p.mkdir(parents=True, exist_ok=True)
        test = p / ".smx_write_test"
        with open(test, "w", encoding="utf-8") as f:
            f.write("ok")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False

def detect_project_root() -> Path:
    """
    Return the consumer project's 'syntaxmatrixdir' folder, creating it if necessary.
    Resolution order:
      1) SMX_CLIENT_DIR (if set and writable)
      2) ./syntaxmatrixdir under current working dir (if writable)
      3) GCS Fuse standard mounts (if present & writable)
      4) /tmp/syntaxmatrixdir (always writable on Cloud Run)
      5) Fallback near the first non-framework caller (if writable)
    """

    # 1) Explicit override (keeps local stable; handy in Cloud Run)
    env = os.environ.get("SMX_CLIENT_DIR")
    if env:
        p = Path(env)
        if _writable(p):
            return p

    # 2) CWD-based
    cwd = Path.cwd()
    p = cwd / "syntaxmatrixdir"
    if _writable(p):
        return p

    # 3) Common GCS Fuse mount points (Gen2)
    for candidate in [Path("/mnt/gcs/syntaxmatrixdir"),
                      Path("/mnt/disks/gcs/syntaxmatrixdir")]:
        if _writable(candidate):
            return candidate

    # 4) Cloud Run safe default
    tmp = Path("/tmp/syntaxmatrixdir")
    if _writable(tmp):
        return tmp

    # 5) Fallback alongside caller
    fallback = scandir() / "syntaxmatrixdir"
    if _writable(fallback):
        return fallback

    # Last resort: return /tmp anyway (avoids import-time crashes)
    return tmp