import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort

import data
from database import (
    init_db, save_message, get_all_messages,
    create_post, get_published_posts, get_pending_posts, get_post_by_slug,
    get_pending_post_by_token, approve_post_by_token, reject_post_by_token,
    approve_post_by_id, delete_post,
)
from mailer import send_contact_email, send_blog_review_email

load_dotenv()  # reads a local .env file if present (see .env.example)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")  # set SECRET_KEY in .env for production

init_db()


def _is_admin() -> bool:
    admin_key = os.environ.get("ADMIN_KEY")
    return bool(admin_key) and request.args.get("key") == admin_key


@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=data.PROFILE,
        education=data.EDUCATION,
        experience=data.EXPERIENCE,
        extras=data.EXTRAS,
    )


@app.route("/skills")
def skills():
    return render_template("skills.html", profile=data.PROFILE, skills=data.SKILLS)


@app.route("/projects")
def projects():
    return render_template("projects.html", profile=data.PROFILE, projects=data.PROJECTS)


@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((p for p in data.PROJECTS if p["slug"] == slug), None)
    if project is None:
        return render_template("404.html", profile=data.PROFILE), 404
    return render_template("project_detail.html", profile=data.PROFILE, project=project)


@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        profile=data.PROFILE,
        education=data.EDUCATION,
        experience=data.EXPERIENCE,
        skills=data.SKILLS,
    )


@app.route("/resume/download")
def resume_download():
    return send_from_directory("static", "resume.pdf", as_attachment=True)


def _normalized_db_post(row):
    """Adapt a DB row to look like the static posts in data.py so both can share templates."""
    return {
        "slug": row["slug"],
        "title": row["title"],
        "date": row["created_at"][:10],
        "excerpt": (row["body"][:160] + "...") if len(row["body"]) > 160 else row["body"],
        "body": [p for p in row["body"].split("\n\n") if p.strip()],
        "author_name": row["author_name"],
    }


@app.route("/blog")
def blog():
    db_posts = [_normalized_db_post(p) for p in get_published_posts()]
    all_posts = sorted(data.BLOG_POSTS + db_posts, key=lambda p: p["date"], reverse=True)
    return render_template("blog.html", profile=data.PROFILE, posts=all_posts)


@app.route("/blog/<slug>")
def blog_post(slug):
    post = next((p for p in data.BLOG_POSTS if p["slug"] == slug), None)
    if post is None:
        db_row = get_post_by_slug(slug)
        post = _normalized_db_post(db_row) if db_row else None
    if post is None:
        return render_template("404.html", profile=data.PROFILE), 404
    return render_template("blog_post.html", profile=data.PROFILE, post=post)


@app.route("/blog/submit", methods=["GET", "POST"])
def blog_submit():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        admin_key = request.form.get("admin_key", "").strip()

        if not name or not email or not title or not body:
            flash("Please fill in every field before submitting.", "error")
            return redirect(url_for("blog_submit"))

        is_owner = bool(os.environ.get("ADMIN_KEY")) and admin_key == os.environ.get("ADMIN_KEY")
        post_id, slug, token = create_post(name, email, title, body, published=is_owner)

        if is_owner:
            flash("Published! Your post is live on the blog.", "success")
        else:
            approve_url = url_for("blog_review", token=token, action="approve", _external=True)
            reject_url = url_for("blog_review", token=token, action="reject", _external=True)
            send_blog_review_email(name, email, title, body, approve_url, reject_url)
            flash("Thanks! Your post has been sent for review and will go live once approved.", "success")

        return redirect(url_for("blog"))

    return render_template("blog_submit.html", profile=data.PROFILE)


@app.route("/blog/review/<token>")
def blog_review(token):
    action = request.args.get("action")
    post = get_pending_post_by_token(token)

    if post is None:
        flash("That review link is invalid or has already been used.", "error")
        return redirect(url_for("blog"))

    if action == "approve":
        approve_post_by_token(token)
        flash(f'"{post["title"]}" is now published.', "success")
    elif action == "reject":
        reject_post_by_token(token)
        flash(f'"{post["title"]}" was rejected and removed.', "success")
    else:
        flash("Unknown review action.", "error")

    return redirect(url_for("blog"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in every field before sending.", "error")
            return redirect(url_for("contact"))

        # 1. Always save first -- the message is never lost even if email fails.
        emailed = send_contact_email(name, email, message)
        save_message(name, email, message, emailed=emailed)

        if emailed:
            flash("Message sent -- thanks for reaching out! I'll get back to you soon.", "success")
        else:
            flash("Message received and saved -- I'll see it soon.", "success")

        return redirect(url_for("contact"))

    return render_template("contact.html", profile=data.PROFILE)


@app.route("/admin/messages")
def admin_messages():
    """
    A simple, private page to review everything saved from the contact form.
    Protected by a shared-secret query param rather than a login system --
    visit /admin/messages?key=YOUR_ADMIN_KEY where YOUR_ADMIN_KEY matches the
    ADMIN_KEY environment variable you set in .env.
    """
    if not _is_admin():
        abort(403)

    messages = get_all_messages()
    return render_template("admin_messages.html", profile=data.PROFILE, messages=messages)


@app.route("/admin/blog")
def admin_blog():
    """Private page to approve/reject pending posts and delete any published post, including your own."""
    if not _is_admin():
        abort(403)

    pending = get_pending_posts()
    published = get_published_posts()
    return render_template(
        "admin_blog.html", profile=data.PROFILE, pending=pending, published=published, key=request.args.get("key")
    )


@app.route("/admin/blog/approve/<int:post_id>")
def admin_blog_approve(post_id):
    if not _is_admin():
        abort(403)
    approve_post_by_id(post_id)
    flash("Post approved and published.", "success")
    return redirect(url_for("admin_blog", key=request.args.get("key")))


@app.route("/admin/blog/delete/<int:post_id>")
def admin_blog_delete(post_id):
    if not _is_admin():
        abort(403)
    delete_post(post_id)
    flash("Post deleted.", "success")
    return redirect(url_for("admin_blog", key=request.args.get("key")))


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html", profile=data.PROFILE), 404


if __name__ == "__main__":
    app.run(debug=True)