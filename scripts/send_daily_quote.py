#!/usr/bin/env python3
"""
Daily Morning Quote Mailer
Runs via GitHub Actions at 10am KST every day.
Uses Claude to select a fresh inspirational quote and emails it.
"""

import anthropic
import smtplib
import os
import json
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def get_quote() -> dict:
    """Ask Claude for an inspirational quote from any source."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": """Pick one powerful, aspirational, pump-you-up quote for someone starting their day.

Pull from absolutely anywhere — movies, books, speeches, interviews, songs, podcasts, TV shows,
conversations, articles, sporting moments, historical events. Be creative and varied;
don't default to the usual suspects every time.

Respond ONLY with a JSON object in this exact format (no markdown, no extra text):
{
  "quote": "the exact quote text",
  "author": "Person's Full Name",
  "source": "brief context, e.g. 'Rocky (1976)', 'The Alchemist by Paulo Coelho', 'Stanford Commencement Speech, 2005', 'Lose Yourself by Eminem', 'The Last Dance documentary', etc."
}"""
            }
        ],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if Claude wraps it anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def build_html(quote_data: dict, day: str) -> str:
    """Build a clean, punchy HTML email body."""
    quote = quote_data["quote"].replace('"', '&ldquo;').replace('"', '&rdquo;')
    author = quote_data["author"]
    source = quote_data["source"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#0d0d0d;font-family:Georgia,'Times New Roman',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0d0d0d;">
    <tr>
      <td align="center" style="padding:40px 20px;">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="padding-bottom:32px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:11px;letter-spacing:3px;
                         text-transform:uppercase;color:#ff6b35;font-weight:700;">
                {day.upper()} MORNING FUEL
              </p>
            </td>
          </tr>

          <!-- Quote block -->
          <tr>
            <td style="border-left:4px solid #ff6b35;padding:8px 0 8px 28px;">
              <p style="margin:0 0 24px 0;font-size:26px;line-height:1.55;
                         font-style:italic;color:#ffffff;font-weight:400;">
                &ldquo;{quote}&rdquo;
              </p>
              <p style="margin:0 0 6px 0;font-size:17px;color:#ff6b35;
                         font-weight:700;font-family:Arial,sans-serif;">
                &mdash;&nbsp;{author}
              </p>
              <p style="margin:0;font-size:13px;color:#666666;font-family:Arial,sans-serif;">
                {source}
              </p>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td style="padding-top:48px;text-align:center;">
              <p style="margin:0;font-size:20px;color:#ffffff;font-family:Arial,sans-serif;
                         letter-spacing:1px;">
                Go get it. 🚀
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding-top:48px;border-top:1px solid #222222;margin-top:48px;">
              <p style="margin:12px 0 0 0;font-size:11px;color:#444444;
                         font-family:Arial,sans-serif;text-align:center;">
                Your daily dose · 10am KST · every single day
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_plain(quote_data: dict, day: str) -> str:
    """Plain-text fallback."""
    return (
        f"{day.upper()} MORNING FUEL\n"
        f"{'=' * 40}\n\n"
        f"\"{quote_data['quote']}\"\n\n"
        f"— {quote_data['author']}\n"
        f"   {quote_data['source']}\n\n"
        f"{'=' * 40}\n"
        f"Go get it. 🚀\n"
    )


def send_email(quote_data: dict) -> None:
    """Send the quote email via Gmail SMTP."""
    gmail_address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = days[datetime.utcnow().weekday()]  # UTC time, close enough for subject line

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔥 {day} Morning Fuel"
    msg["From"] = f"Morning Fuel <{gmail_address}>"
    msg["To"] = recipient

    msg.attach(MIMEText(build_plain(quote_data, day), "plain"))
    msg.attach(MIMEText(build_html(quote_data, day), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, app_password)
        server.sendmail(gmail_address, recipient, msg.as_string())

    print(f"✅  Sent to {recipient}")
    print(f"📖  \"{quote_data['quote']}\"")
    print(f"✍️   — {quote_data['author']} ({quote_data['source']})")


def main() -> None:
    required = ["ANTHROPIC_API_KEY", "GMAIL_ADDRESS", "GMAIL_APP_PASSWORD", "RECIPIENT_EMAIL"]
    missing = [v for v in required if not os.environ.get(v)]
    if missing:
        print(f"❌  Missing env vars: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    print("🤖  Asking Claude for today's quote…")
    quote_data = get_quote()

    print("📬  Sending email…")
    send_email(quote_data)


if __name__ == "__main__":
    main()
