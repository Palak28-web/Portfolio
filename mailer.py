"""
Sends contact-form submissions to you by email over SMTP.

Configure via environment variables (see .env.example):
  SMTP_HOST      -- e.g. smtp.gmail.com (default: smtp.gmail.com)
  SMTP_PORT      -- e.g. 587 (default: 587)
  SMTP_USER      -- the mailbox that sends the email (e.g. your Gmail address)
  SMTP_PASSWORD  -- an app password for that mailbox (NOT your normal login password)
  MAIL_TO        -- where you want to receive messages (defaults to SMTP_USER)

If SMTP_USER / SMTP_PASSWORD aren't set, sending is skipped and the message
stays safely in the database -- the contact form never breaks because of a
missing or wrong email configuration.
"""
import os
import smtplib
from email.message import EmailMessage


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
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    mail_to = os.environ.get("MAIL_TO", smtp_user)

    if not smtp_user or not smtp_password:
        print("[mailer] SMTP_USER / SMTP_PASSWORD not set -- skipping email send (data is still saved to the database).")
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
        print(f"[mailer] Failed to send email: {e}")
        return False