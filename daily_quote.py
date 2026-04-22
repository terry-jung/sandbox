#!/usr/bin/env python3
"""Daily inspirational quote emailer — generates via Claude API, sends via Gmail SMTP."""

import os
import smtplib
import ssl
import json
import re
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import zoneinfo

import anthropic

RECIPIENT = "thjung91@gmail.com"
SENDER = "thjung91@gmail.com"
TIMEZONE = zoneinfo.ZoneInfo("Asia/Seoul")
CONFIG_FILE = os.path.expanduser("~/.daily_quote.env")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_FILE}\n"
            "Create it with: GMAIL_APP_PASSWORD=your_16_char_password"
        )
    config = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    return config


def generate_quote():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now(TIMEZONE).strftime("%A, %B %d, %Y")

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Give me ONE powerful, aspirational, "
                    "pump-you-up quote from ANY source — a movie, book, speech, song, "
                    "interview, sports moment, poem, show, anything. "
                    "Pick something unexpected and electrifying, not the usual clichés. "
                    "Format your response as exactly two lines:\n"
                    'Line 1: The quote in double quotes\n'
                    "Line 2: — Attribution (Source type: e.g. film, novel, speech, song)\n"
                    "Nothing else. No intro, no commentary."
                ),
            }
        ],
    )

    text = message.content[0].text.strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) >= 2:
        quote_line = lines[0].strip('"').strip()
        attribution = lines[1].lstrip("—").strip()
    else:
        quote_line = text
        attribution = "Unknown"
    return quote_line, attribution


def build_email(quote, attribution):
    today = datetime.now(TIMEZONE).strftime("%A, %B %d")
    subject = f"☀️ Morning Fuel — {today}"

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Georgia, serif; background: #fafaf8; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 600px; margin: 40px auto; background: #fff;
                border-radius: 12px; overflow: hidden;
                box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
    .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
               padding: 40px 48px 32px; }}
    .day {{ color: #e0a84b; font-size: 13px; letter-spacing: 3px;
            text-transform: uppercase; margin-bottom: 8px; }}
    .header h1 {{ color: #fff; font-size: 22px; margin: 0;
                  font-weight: normal; letter-spacing: 1px; }}
    .body {{ padding: 48px; }}
    .quote {{ font-size: 26px; line-height: 1.5; color: #1a1a2e;
              font-style: italic; margin: 0 0 28px; }}
    .quote::before {{ content: '“'; font-size: 60px; color: #e0a84b;
                      line-height: 0; vertical-align: -0.4em;
                      margin-right: 4px; font-style: normal; }}
    .attribution {{ color: #666; font-size: 15px; padding-top: 20px;
                    border-top: 2px solid #f0ede8; }}
    .footer {{ padding: 24px 48px; background: #f7f5f0;
               color: #999; font-size: 12px; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="day">{today}</div>
      <h1>Your Morning Fuel</h1>
    </div>
    <div class="body">
      <p class="quote">{quote}</p>
      <p class="attribution">— {attribution}</p>
    </div>
    <div class="footer">Delivered daily at 10am KST &nbsp;·&nbsp; Go crush it today.</div>
  </div>
</body>
</html>
"""
    text = f'"{quote}"\n\n— {attribution}\n\nGo crush it today.'
    return subject, html, text


def send_email(subject, html, text, app_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, app_password)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())


def run():
    config = load_config()
    app_password = config.get("GMAIL_APP_PASSWORD", "")
    if not app_password:
        raise ValueError("GMAIL_APP_PASSWORD not set in ~/.daily_quote.env")

    print(f"[{datetime.now(TIMEZONE).strftime('%H:%M:%S')}] Generating quote...")
    quote, attribution = generate_quote()
    print(f'Quote: "{quote}" — {attribution}')

    subject, html, text = build_email(quote, attribution)
    send_email(subject, html, text, app_password)
    print(f"[{datetime.now(TIMEZONE).strftime('%H:%M:%S')}] Sent to {RECIPIENT}")


if __name__ == "__main__":
    run()
