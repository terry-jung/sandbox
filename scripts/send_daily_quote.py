#!/usr/bin/env python3
import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

RECIPIENT_EMAIL = "thjung91@gmail.com"
SENDER_EMAIL = os.environ["GMAIL_SENDER_EMAIL"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

def get_quote() -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%A, %B %d, %Y")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Give me one powerful, aspirational, pump-you-up quote "
                    "that will make someone feel fired up and ready to conquer the day. "
                    "The quote can be from anyone — a movie character, athlete, entrepreneur, "
                    "philosopher, musician, fictional character, podcast, speech, book, anything. "
                    "Pick someone unexpected and interesting, not the same tired names. "
                    "Vary the tone: sometimes fierce, sometimes tender, sometimes funny, "
                    "sometimes philosophical. Make it feel fresh and personally chosen for today.\n\n"
                    "Respond ONLY in this exact format (no extra text):\n"
                    'QUOTE: "the quote here"\n'
                    "SOURCE: Name, context (e.g. movie title, book, speech at X, interview with Y)"
                ),
            }
        ],
    )

    raw = message.content[0].text.strip()
    lines = raw.splitlines()

    quote = ""
    source = ""
    for line in lines:
        if line.startswith("QUOTE:"):
            quote = line[len("QUOTE:"):].strip().strip('"')
        elif line.startswith("SOURCE:"):
            source = line[len("SOURCE:"):].strip()

    return {"quote": quote, "source": source}


def build_email(quote: str, source: str) -> MIMEMultipart:
    today_label = datetime.now().strftime("%A, %B %d")

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
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .header {{
      padding: 32px 40px 16px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .day-label {{
      font-family: 'Helvetica Neue', sans-serif;
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #e94560;
      margin-bottom: 6px;
    }}
    .header-title {{
      font-size: 20px;
      color: rgba(255,255,255,0.85);
      font-weight: 400;
    }}
    .body {{
      padding: 48px 40px;
    }}
    .quote-mark {{
      font-size: 80px;
      line-height: 0.5;
      color: #e94560;
      opacity: 0.6;
      font-family: Georgia, serif;
    }}
    .quote-text {{
      font-size: 24px;
      line-height: 1.6;
      color: #ffffff;
      margin: 24px 0 32px;
      font-style: italic;
    }}
    .source {{
      font-family: 'Helvetica Neue', sans-serif;
      font-size: 13px;
      color: #e94560;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    .footer {{
      padding: 20px 40px;
      background: rgba(0,0,0,0.2);
      font-family: 'Helvetica Neue', sans-serif;
      font-size: 11px;
      color: rgba(255,255,255,0.3);
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="day-label">{today_label}</div>
      <div class="header-title">Your Morning Fuel</div>
    </div>
    <div class="body">
      <div class="quote-mark">&ldquo;</div>
      <div class="quote-text">{quote}</div>
      <div class="source">— {source}</div>
    </div>
    <div class="footer">Go out there and make it happen.</div>
  </div>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Morning Quote — {today_label}"
    msg["From"] = f"Morning Fuel <{SENDER_EMAIL}>"
    msg["To"] = RECIPIENT_EMAIL

    plain = f'"{quote}"\n\n— {source}\n\nGo out there and make it happen.'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))
    return msg


def send_email(msg: MIMEMultipart) -> None:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())


def main():
    print("Generating quote...")
    data = get_quote()
    print(f"Quote: {data['quote']}")
    print(f"Source: {data['source']}")

    msg = build_email(data["quote"], data["source"])
    print("Sending email...")
    send_email(msg)
    print("Done. Quote delivered.")


if __name__ == "__main__":
    main()
