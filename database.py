"""
Persists contact-form submissions AND community blog-post submissions to a
local SQLite database (messages.db).
"""
import re
import secrets
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "messages.db"


def init_db():
    """Create tables if they don't exist yet. Safe to call on every startup."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                emailed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE,
                title TEXT NOT NULL,
                author_name TEXT NOT NULL,
                author_email TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                token TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def save_message(name: str, email: str, message: str, emailed: bool = False) -> int:
    """Insert a new contact-form message and return its row id."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO messages (name, email, message, created_at, emailed) VALUES (?, ?, ?, ?, ?)",
            (name, email, message, datetime.now(timezone.utc).isoformat(), int(emailed)),
        )
        return cursor.lastrowid


def get_all_messages():
    """Return every saved contact-form message, newest first."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Blog posts
# ---------------------------------------------------------------------------

def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "post"


def create_post(name: str, email: str, title: str, body: str, published: bool):
    """
    Create a blog post. If published=True (i.e. the correct admin key was
    supplied), it goes live immediately and no token is needed. Otherwise it's
    saved as 'pending' with a random, unguessable review token used in the
    approve/reject email links.

    Returns (post_id, slug, token). token is None for published posts.
    """
    status = "published" if published else "pending"
    token = None if published else secrets.token_urlsafe(32)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO blog_posts (slug, title, author_name, author_email, body, status, token, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (None, title, name, email, body, status, token, datetime.now(timezone.utc).isoformat()),
        )
        post_id = cursor.lastrowid
        slug = f"{_slugify(title)}-{post_id}"
        conn.execute("UPDATE blog_posts SET slug = ? WHERE id = ?", (slug, post_id))
    return post_id, slug, token


def get_published_posts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM blog_posts WHERE status = 'published' ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_pending_posts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM blog_posts WHERE status = 'pending' ORDER BY created_at ASC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_post_by_slug(slug: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM blog_posts WHERE slug = ? AND status = 'published'", (slug,)
        ).fetchone()
        return dict(row) if row else None


def get_pending_post_by_token(token: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM blog_posts WHERE token = ? AND status = 'pending'", (token,)
        ).fetchone()
        return dict(row) if row else None


def approve_post_by_token(token: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE blog_posts SET status = 'published', token = NULL WHERE token = ? AND status = 'pending'",
            (token,),
        )
        return cursor.rowcount > 0


def reject_post_by_token(token: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "DELETE FROM blog_posts WHERE token = ? AND status = 'pending'", (token,)
        )
        return cursor.rowcount > 0


def approve_post_by_id(post_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE blog_posts SET status = 'published', token = NULL WHERE id = ? AND status = 'pending'",
            (post_id,),
        )
        return cursor.rowcount > 0


def delete_post(post_id: int) -> bool:
    """Deletes a post regardless of status -- used by the admin page to remove any post, including your own."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM blog_posts WHERE id = ?", (post_id,))
        return cursor.rowcount > 0