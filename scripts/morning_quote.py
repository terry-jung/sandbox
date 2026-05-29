#!/usr/bin/env python3
import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

RECIPIENT = "thjung91@gmail.com"
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]


def generate_quote() -> tuple[str, str, str]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "Give me one aspirational, inspirational, pump-you-up quote "
                    "that will make someone feel fired up and ready to conquer the day. "
                    "It can come from anywhere — a movie, book, speech, song, podcast, "
                    "interview, conversation, article, anything. "
                    "Pick something powerful, varied, and unexpected (not the same tired classics). "
                    "Respond in exactly this format:\n"
                    'QUOTE: "The exact quote here"\n'
                    "SOURCE: Who said/wrote/sang it, and the source (e.g., Movie, Book, Speech, Song)\n"
                    "CONTEXT: One sentence on why this quote hits different."
                ),
            }
        ],
    )

    text = message.content[0].text.strip()
    lines = {
        line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
        for line in text.splitlines()
        if ":" in line
    }
    quote = lines.get("QUOTE", "").strip('"')
    source = lines.get("SOURCE", "")
    context = lines.get("CONTEXT", "")
    return quote, source, context


def build_html(quote: str, source: str, context: str, date_str: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0f0f0f;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f0f;padding:40px 20px;">
    <tr><td align="center">
      <table width="580" cellpadding="0" cellspacing="0" style="background:#1a1a1a;border-radius:16px;overflow:hidden;">

        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#ff6b35,#f7c59f);padding:32px 40px;text-align:center;">
            <p style="margin:0;font-size:12px;font-weight:700;letter-spacing:4px;color:#1a1a1a;text-transform:uppercase;">Good Morning ☀️</p>
            <p style="margin:8px 0 0;font-size:13px;color:#3d2b1a;opacity:0.8;">{date_str}</p>
          </td>
        </tr>

        <!-- Quote -->
        <tr>
          <td style="padding:48px 48px 32px;">
            <p style="margin:0 0 8px;font-size:36px;color:#ff6b35;line-height:1;">&ldquo;</p>
            <p style="margin:0;font-size:22px;line-height:1.6;color:#f0ece4;font-style:italic;font-weight:500;">
              {quote}
            </p>
            <p style="margin:0;font-size:36px;color:#ff6b35;line-height:1;text-align:right;">&rdquo;</p>
          </td>
        </tr>

        <!-- Source -->
        <tr>
          <td style="padding:0 48px 24px;">
            <p style="margin:0;font-size:14px;font-weight:700;color:#ff6b35;letter-spacing:1px;">— {source}</p>
          </td>
        </tr>

        <!-- Divider -->
        <tr>
          <td style="padding:0 48px;">
            <hr style="border:none;border-top:1px solid #2e2e2e;margin:0;">
          </td>
        </tr>

        <!-- Context -->
        <tr>
          <td style="padding:24px 48px 48px;">
            <p style="margin:0;font-size:14px;line-height:1.7;color:#888;font-style:italic;">{context}</p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#111;padding:20px 40px;text-align:center;">
            <p style="margin:0;font-size:12px;color:#444;letter-spacing:2px;text-transform:uppercase;">Go get it. Today is yours.</p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def send_email(quote: str, source: str, context: str) -> None:
    kst_now = datetime.utcnow()
    date_str = kst_now.strftime("%A, %B %-d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Morning Fuel ⚡ — {date_str}"
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT

    plain = f'"{quote}"\n\n— {source}\n\n{context}\n\nGo get it. Today is yours.'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(build_html(quote, source, context, date_str), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())
        print(f"Sent: {quote[:60]}...")


if __name__ == "__main__":
    quote, source, context = generate_quote()
    send_email(quote, source, context)
