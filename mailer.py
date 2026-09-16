# """
# Sends contact-form submissions to you by email over SMTP.

# Configure via environment variables (see .env.example):
#   SMTP_HOST      -- e.g. smtp.gmail.com (default: smtp.gmail.com)
#   SMTP_PORT      -- e.g. 587 (default: 587)
#   SMTP_USER      -- the mailbox that sends the email (e.g. your Gmail address)
#   SMTP_PASSWORD  -- an app password for that mailbox (NOT your normal login password)
#   MAIL_TO        -- where you want to receive messages (defaults to SMTP_USER)

# If SMTP_USER / SMTP_PASSWORD aren't set, sending is skipped and the message
# stays safely in the database -- the contact form never breaks because of a
# missing or wrong email configuration.
# """
# import os
# import smtplib
# from email.message import EmailMessage


# def send_contact_email(name: str, sender_email: str, message_body: str) -> bool:
#     return _send_email(
#         subject=f"Portfolio contact form: {name}",
#         body=f"From: {name} <{sender_email}>\n\n{message_body}",
#         reply_to=sender_email,
#     )


# def send_blog_review_email(name: str, sender_email: str, title: str, body: str, approve_url: str, reject_url: str) -> bool:
#     email_body = (
#         f"{name} <{sender_email}> wants to publish a blog post on your portfolio.\n\n"
#         f"Title: {title}\n\n"
#         f"{body}\n\n"
#         "--------------------------------------------\n"
#         f"Approve and publish it:\n{approve_url}\n\n"
#         f"Reject it (deletes the submission):\n{reject_url}\n"
#     )
#     return _send_email(
#         subject=f"Blog post awaiting your approval: {title}",
#         body=email_body,
#         reply_to=sender_email,
#     )


# def _send_email(subject: str, body: str, reply_to: str) -> bool:
#     smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
#     smtp_port = int(os.environ.get("SMTP_PORT", "587"))
#     smtp_user = os.environ.get("SMTP_USER")
#     smtp_password = os.environ.get("SMTP_PASSWORD")
#     mail_to = os.environ.get("MAIL_TO", smtp_user)

#     if not smtp_user or not smtp_password:
#         print("[mailer] SMTP_USER / SMTP_PASSWORD not set -- skipping email send (data is still saved to the database).")
#         return False

#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = smtp_user
#     msg["To"] = mail_to
#     msg["Reply-To"] = reply_to
#     msg.set_content(body)

#     try:
#         with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
#             server.starttls()
#             server.login(smtp_user, smtp_password)
#             server.send_message(msg)
#         return True
#     except Exception as e:
#         print(f"[mailer] Failed to send email: {e}")
#         return False


"""
Sends contact-form and blog-review emails to you.

Primary path: the Resend HTTP API (https://resend.com), configured via:
  RESEND_API_KEY -- your Resend API key
  FROM_EMAIL     -- sender address (defaults to "onboarding@resend.dev", a
                    shared test address Resend provides -- no domain setup
                    needed to get started)
  MAIL_TO        -- where you want to receive messages

This uses plain HTTPS, so it works on hosts like Render's free tier that
block outbound SMTP ports (587/465). If Render's outbound SMTP is later
allowed on your plan, or you're just testing locally, plain SMTP still works
as a fallback -- see the SMTP_* variables below -- but Resend is what's
recommended for production.

If neither RESEND_API_KEY nor SMTP_USER/SMTP_PASSWORD are configured, sending
is skipped and the message stays safely in the database -- the contact form
never breaks because of a missing or wrong email configuration.
"""
import os
import smtplib
from email.message import EmailMessage

import requests


def send_contact_email(name: str, sender_email: str, message_body: str) -> bool:
    return _send_email(
        subject=f"Portfolio contact form: {name}",
        body=f"From: {name} <{sender_email}>\n\n{message_body}",
        reply_to=sender_email,
    )


def send_blog_review_email(name: str, sender_email: str, title: str, body: str, approve_url: str, reject_url: str) -> bool:
    email_body = (
        f"{name} <{sender_email}> wants to publish a blog post on your portfolio.\n\n"
        f"Title: {title}\n\n"
        f"{body}\n\n"
        "--------------------------------------------\n"
        f"Approve and publish it:\n{approve_url}\n\n"
        f"Reject it (deletes the submission):\n{reject_url}\n"
    )
    return _send_email(
        subject=f"Blog post awaiting your approval: {title}",
        body=email_body,
        reply_to=sender_email,
    )


def _send_email(subject: str, body: str, reply_to: str) -> bool:
    resend_api_key = os.environ.get("RESEND_API_KEY")
    if resend_api_key:
        return _send_via_resend(resend_api_key, subject, body, reply_to)
    return _send_via_smtp(subject, body, reply_to)


def _send_via_resend(api_key: str, subject: str, body: str, reply_to: str) -> bool:
    from_email = os.environ.get("FROM_EMAIL", "onboarding@resend.dev")
    mail_to = os.environ.get("MAIL_TO")

    if not mail_to:
        print("[mailer] MAIL_TO not set -- skipping email send (data is still saved to the database).")
        return False

    try:
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "from": from_email,
                "to": [mail_to],
                "reply_to": reply_to,
                "subject": subject,
                "text": body,
            },
            timeout=10,
        )
        if resp.status_code >= 400:
            print(f"[mailer] Resend API error {resp.status_code}: {resp.text}")
            return False
        return True
    except Exception as e:
        print(f"[mailer] Failed to send via Resend: {e}")
        return False


def _send_via_smtp(subject: str, body: str, reply_to: str) -> bool:
    """Local-dev fallback only -- many hosts (including Render's free tier) block outbound SMTP."""
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    mail_to = os.environ.get("MAIL_TO", smtp_user)

    if not smtp_user or not smtp_password:
        print("[mailer] No email provider configured (RESEND_API_KEY or SMTP_USER/SMTP_PASSWORD) -- skipping email send (data is still saved to the database).")
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = mail_to
    msg["Reply-To"] = reply_to
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[mailer] Failed to send via SMTP: {e}")
        return False