#!/usr/bin/env python3
"""Sends a daily aspirational quote via Gmail using Claude to generate it."""

import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import anthropic
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]


def generate_quote() -> tuple[str, str]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%A, %B %d")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Give me ONE powerful, aspirational quote that will make someone feel "
                    "pumped, energized, and ready to take on the day. "
                    "The quote can be from absolutely anything — a movie, book, speech, song, podcast, interview, "
                    "conversation, article, TV show, sports moment, anything. "
                    "Be creative and varied — don't always pick the most famous quotes. "
                    "Surprise me. Mix eras, cultures, and sources. "
                    "Respond in EXACTLY this format (nothing else):\n"
                    "QUOTE: <the quote>\n"
                    "SOURCE: <who said/wrote/sang it, and where it's from>"
                ),
            }
        ],
    )

    text = message.content[0].text.strip()
    quote = ""
    source = ""
    for line in text.splitlines():
        if line.startswith("QUOTE:"):
            quote = line.removeprefix("QUOTE:").strip()
        elif line.startswith("SOURCE:"):
            source = line.removeprefix("SOURCE:").strip()
    return quote, source


def build_email(quote: str, source: str) -> MIMEMultipart:
    day_str = datetime.now().strftime("%A, %B %d")

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      margin: 0; padding: 0;
      background: #0f0f0f;
      font-family: 'Georgia', serif;
    }}
    .wrapper {{
      max-width: 600px;
      margin: 40px auto;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      border-radius: 16px;
      padding: 48px 40px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .date {{
      color: #e94560;
      font-size: 13px;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 32px;
    }}
    .quote-mark {{
      font-size: 80px;
      color: #e94560;
      line-height: 0.5;
      display: block;
      margin-bottom: 24px;
    }}
    .quote {{
      color: #f0f0f0;
      font-size: 24px;
      line-height: 1.6;
      font-style: italic;
      margin: 0 0 32px 0;
    }}
    .divider {{
      width: 48px;
      height: 3px;
      background: #e94560;
      margin-bottom: 20px;
    }}
    .source {{
      color: #a0a8c0;
      font-size: 15px;
      letter-spacing: 0.5px;
    }}
    .footer {{
      margin-top: 48px;
      color: #3a4060;
      font-size: 12px;
      text-align: center;
      font-family: sans-serif;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="date">{day_str}</div>
    <span class="quote-mark">&ldquo;</span>
    <p class="quote">{quote}</p>
    <div class="divider"></div>
    <div class="source">— {source}</div>
    <div class="footer">Your daily dose of fuel. Go crush it. 🔥</div>
  </div>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚡ Your Morning Quote — {day_str}"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg.attach(MIMEText(f'"{quote}"\n\n— {source}', "plain"))
    msg.attach(MIMEText(html, "html"))
    return msg


def send_email(msg: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())


def main() -> None:
    quote, source = generate_quote()
    msg = build_email(quote, source)
    send_email(msg)
    print(f"[{datetime.now().isoformat()}] Quote sent: \"{quote}\" — {source}")


if __name__ == "__main__":
    main()
