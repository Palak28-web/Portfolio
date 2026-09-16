# Palak Jangir -- Portfolio (Flask)

A dark, IDE-inspired personal portfolio built with Flask.

## Run it locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Project layout

```
portfolio/
├── app.py                  # Routes
├── data.py                 # All your content -- edit this to update the site
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── resume.pdf          # Your actual resume, served via the Download button
└── templates/              # Jinja2 templates (one per page)
```

## Making it yours

- **Update content**: everything -- your summary, experience, skills, projects, blog
  posts -- lives in `data.py` as plain Python lists/dicts. Edit that file and the
  site updates automatically; you don't need to touch any HTML.
- **Replace the resume**: swap `static/resume.pdf` with a new export whenever you
  update your resume. The "Download PDF" buttons already point at this file.
- **Add a real project**: add another dict to the `PROJECTS` list in `data.py`
  with a unique `slug` -- a detail page is generated automatically at
  `/projects/<slug>`.
- **Blog moderation**: your blog now takes public submissions at `/blog/submit`.
  - If the submitter enters the correct `ADMIN_KEY` in the (hidden-by-default)
    "Owner key" field, the post publishes instantly -- that's how *you* post
    without waiting on approval.
  - Anyone else's submission is saved as pending and you get an email with
    one-click **Approve** / **Reject** links (no login needed -- the link
    itself is a private, single-use token).
  - Manage everything -- approve, reject, or delete any post you've published
    -- at `/admin/blog?key=YOUR_ADMIN_KEY`.
  - Note: the sample posts baked into `BLOG_POSTS` in `data.py` are separate
    from submitted posts and aren't deletable from the admin page -- edit or
    remove them directly in `data.py` instead.
- **Contact form messages**: every submission is saved to a local SQLite
  database (`messages.db`, created automatically) and emailed to you via SMTP.
  1. Copy `.env.example` to `.env` and fill in your real values.
  2. For Gmail: turn on 2-Step Verification, then create an "App Password" at
     https://myaccount.google.com/apppasswords and use that as `SMTP_PASSWORD`
     (not your normal Gmail password).
  3. If you skip this setup, messages are still saved to the database --
     nothing is ever lost, email is just an extra delivery channel.
  4. Review saved messages any time at `/admin/messages?key=YOUR_ADMIN_KEY`
     (set `ADMIN_KEY` in `.env` first). Don't share this URL publicly.
- **Add a profile photo**: drop a square-cropped image at
  `static/img/profile.jpg` (~400x400px works well), then uncomment the
  `<img>` line near the top of the hero section in `templates/index.html`.
  CSS for sizing it neatly is already in place.
- **Favicon**: the browser-tab icon is a small "PJ" monogram matching the
  sidebar badge (`static/img/favicon.svg`, with PNG fallbacks). Replace those
  files if you'd rather use a different mark or your photo.

## Deploying

This is a standard Flask app, so it deploys anywhere Flask does -- Azure Web
Apps, Render, Railway, PythonAnywhere, or a VPS behind gunicorn + nginx. For
production, set a real `app.secret_key` (currently a placeholder in `app.py`)
and turn off debug mode.

**Not Vercel:** Vercel runs Python apps as serverless functions with a
read-only, ephemeral filesystem, so `messages.db` can't reliably persist
there. Render is the closest free platform with a similar "connect GitHub,
auto-deploy" workflow that actually keeps your files.

**On Render's free tier specifically:**
- The service "spins down" after ~15 minutes of no traffic and takes 30-60
  seconds to wake back up on the next visit -- normal for a low-traffic
  personal portfolio, just don't be surprised by the first slow load.
- The free tier's disk is generally stable across restarts, but isn't
  guaranteed to survive every redeploy. For a personal portfolio this is
  usually fine, but if `messages.db` ever matters a lot to you, consider
  Render's paid persistent disk add-on, or swapping SQLite for a small hosted
  database (e.g. a free Postgres instance) down the line.
- The admin routes (`/admin/messages`, `/admin/blog`) work exactly the same
  once deployed -- just use `https://your-app.onrender.com/admin/blog?key=...`
  instead of `127.0.0.1:5000`.


## to manage the approvals rejections and the delteion of blog post go here
url/admin/blog?key=Your admin key