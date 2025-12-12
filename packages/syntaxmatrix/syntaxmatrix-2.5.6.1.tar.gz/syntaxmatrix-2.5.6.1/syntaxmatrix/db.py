from __future__ import annotations
import sqlite3
import os
import json
from werkzeug.utils import secure_filename
from syntaxmatrix.project_root import detect_project_root


_CLIENT_DIR = detect_project_root()
DB_PATH = os.path.join(_CLIENT_DIR, "data", "syntaxmatrix.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

TEMPLATES_DIR = os.path.join(_CLIENT_DIR, "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)


# ***************************************
# Pages Table Functions
# ***************************************
def init_db():
    conn = sqlite3.connect(DB_PATH)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            name TEXT PRIMARY KEY,
            content TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS askai_cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            question TEXT,
            output TEXT,
            code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_pages():
    """Return {page_name: html} resolving relative paths under syntaxmatrixdir/templates."""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT name, content FROM pages").fetchall()
    conn.close()

    pages = {}
    for name, file_path in rows:
        # If the DB holds a relative path (e.g. 'templates/about.html'), make it absolute.
        if file_path and not os.path.isabs(file_path):
            file_path = os.path.join(_CLIENT_DIR, file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                pages[name] = f.read()
        except Exception:
            pages[name] = f"<p>Missing file for page '{name}'.</p>"
    return pages


def add_page(name, html):
    """Create templates/<slug>.html and store a relative path in the DB."""
    filename = secure_filename(name.lower()) + ".html"
    abs_path = os.path.join(TEMPLATES_DIR, filename)

    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(html)

    rel_path = f"templates/{filename}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO pages (name, content) VALUES (?, ?)", (name, rel_path))

    conn.commit()
    conn.close()


def update_page(old_name, new_name, html):
    """
    Overwrite the page file; if the title changes, rename the file.
    Always store a relative path 'templates/<slug>.html' in the DB.
    """
    import sqlite3, os
    from werkzeug.utils import secure_filename

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    row = cur.execute("SELECT content FROM pages WHERE name = ?", (old_name,)).fetchone()
    if not row:
        conn.close()
        return

    # Resolve current path (absolute if DB stored absolute; otherwise under syntaxmatrixdir)
    current = row[0] or ""
    if current and not os.path.isabs(current):
        current_abs = os.path.join(_CLIENT_DIR, current)
    else:
        current_abs = current

    # Target filename/path for the new name
    new_filename = secure_filename(new_name.lower()) + ".html"
    target_abs   = os.path.join(_CLIENT_DIR, "templates", new_filename)
    os.makedirs(os.path.dirname(target_abs), exist_ok=True)

    # If name changed and the old file exists, rename; otherwise we’ll just write fresh
    if old_name != new_name and current_abs and os.path.exists(current_abs) and current_abs != target_abs:
        try:
            os.replace(current_abs, target_abs)
        except Exception:
            # If rename fails (e.g. old file missing), we’ll write the new file below
            pass

    # Write the HTML (create if missing, overwrite if present)
    with open(target_abs, "w", encoding="utf-8") as f:
        f.write(html)

    # Store a relative, OS-agnostic path in the DB
    rel_path = f"templates/{new_filename}"
    cur.execute(
        "UPDATE pages SET name = ?, content = ? WHERE name = ?",
        (new_name, rel_path, old_name)
    )
    conn.commit()
    conn.close()

def delete_page(name):
    """
    Delete the page file (if present) and remove the row from the DB.
    Works whether 'content' is absolute or relative.
    """
    import sqlite3, os

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    row = cur.execute("SELECT content FROM pages WHERE name = ?", (name,)).fetchone()
    if row:
        path = row[0] or ""
        abs_path = path if os.path.isabs(path) else os.path.join(_CLIENT_DIR, path)
        if os.path.exists(abs_path):
            try:
                os.remove(abs_path)
            except Exception:
                # Don’t block deletion if the file cannot be removed
                pass

    cur.execute("DELETE FROM pages WHERE name = ?", (name,))
    conn.commit()
    conn.close()