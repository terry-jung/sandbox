#!/usr/bin/env python3
"""Generates a daily inspirational quote via Claude and emails it."""

import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import anthropic

PROMPT = """Pick one genuinely powerful, energising quote for someone starting their day.

Rules:
- The quote must feel fresh and punchy — avoid the most overused classics (no "be the change", no "shoot for the moon", etc.)
- It can come from ANYWHERE: a movie, a song lyric, a novel, a speech, a podcast, an interview, a conversation, a manifesto, an article — get creative with the source
- Include the exact source context (e.g. character name + film, chapter + book title, time stamp + podcast name, song title + artist)
- The tone should be warm and energising, not preachy

Respond in this exact format (no extra text):
QUOTE: "<the quote>"
SOURCE: <who said/wrote/sang/spoke it and where>
"""


def generate_quote() -> tuple[str, str]:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=300,
        messages=[{"role": "user", "content": PROMPT}],
    )
    text = message.content[0].text.strip()

    quote, source = "", ""
    for line in text.splitlines():
        if line.startswith("QUOTE:"):
            quote = line[len("QUOTE:"):].strip().strip('"')
        elif line.startswith("SOURCE:"):
            source = line[len("SOURCE:"):].strip()

    return quote, source


def build_email(quote: str, source: str) -> tuple[str, str]:
    today = datetime.now().strftime("%A, %B %-d")
    subject = f"Your morning quote — {today}"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Georgia, serif; background: #fafaf8; margin: 0; padding: 0; }}
    .wrap {{ max-width: 560px; margin: 48px auto; background: #fff;
              border-radius: 12px; overflow: hidden;
              box-shadow: 0 2px 12px rgba(0,0,0,.08); }}
    .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
               padding: 32px 40px; }}
    .header h1 {{ color: #e8c96d; margin: 0; font-size: 13px;
                  letter-spacing: 3px; text-transform: uppercase; }}
    .header p  {{ color: #8899aa; margin: 6px 0 0; font-size: 13px; }}
    .body {{ padding: 40px; }}
    blockquote {{ margin: 0 0 24px; border-left: 4px solid #e8c96d;
                  padding: 4px 0 4px 20px; }}
    blockquote p {{ font-size: 22px; line-height: 1.5; color: #1a1a2e;
                    margin: 0; font-style: italic; }}
    .source {{ color: #667788; font-size: 14px; margin-top: 8px; }}
    .footer {{ padding: 24px 40px; background: #f5f5f0;
               color: #aaa; font-size: 12px; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <h1>Good morning</h1>
      <p>{today}</p>
    </div>
    <div class="body">
      <blockquote>
        <p>{quote}</p>
      </blockquote>
      <p class="source">— {source}</p>
    </div>
    <div class="footer">Have an amazing day. You've got this.</div>
  </div>
</body>
</html>"""

    return subject, html


def send_email(subject: str, html: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Quote sent to {recipient}")


if __name__ == "__main__":
    quote, source = generate_quote()
    subject, html = build_email(quote, source)
    send_email(subject, html)
    print(f"Quote: {quote}")
    print(f"Source: {source}")
