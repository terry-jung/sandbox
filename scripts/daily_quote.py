import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SYSTEM_PROMPT = """You are a curator of powerful, soul-stirring quotes.
Your job is to select ONE quote that will fire someone up and make them feel ready to conquer the day.

Rules:
- The quote must be real and accurately attributed
- Draw from ANY source: movies, books, speeches, songs, podcasts, interviews, conversations, athletes, leaders, artists, philosophers, fictional characters — anything
- Vary the source type and person each day (don't repeat patterns)
- Choose quotes that are visceral, bold, and energizing — not generic platitudes
- Respond ONLY in this exact format, nothing else:

QUOTE: [the quote]
SOURCE: [person's name]
CONTEXT: [1 sentence: where it's from — movie title, book name, speech occasion, etc.]"""

def generate_quote() -> dict:
    client = anthropic.Anthropic()

    today = datetime.now().strftime("%A, %B %d")
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Today is {today}. Give me the quote."
            }
        ]
    )

    raw = message.content[0].text.strip()
    lines = {line.split(": ", 1)[0]: line.split(": ", 1)[1]
             for line in raw.splitlines() if ": " in line}

    return {
        "quote": lines.get("QUOTE", ""),
        "source": lines.get("SOURCE", ""),
        "context": lines.get("CONTEXT", ""),
    }


def build_email_html(quote: str, source: str, context: str) -> str:
    today = datetime.now().strftime("%A, %B %d")
    return f"""
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
    .container {{
      max-width: 600px;
      margin: 40px auto;
      background: #1a1a1a;
      border-radius: 12px;
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #ff6b35, #f7c59f);
      padding: 28px 36px 20px;
      color: #0f0f0f;
    }}
    .header .label {{
      font-size: 11px;
      font-family: 'Courier New', monospace;
      letter-spacing: 3px;
      text-transform: uppercase;
      opacity: 0.7;
      margin-bottom: 4px;
    }}
    .header .date {{
      font-size: 22px;
      font-weight: bold;
    }}
    .body {{
      padding: 40px 36px 32px;
    }}
    .quote {{
      font-size: 22px;
      line-height: 1.6;
      color: #f5f0e8;
      font-style: italic;
      margin: 0 0 28px;
      border-left: 3px solid #ff6b35;
      padding-left: 20px;
    }}
    .attribution {{
      color: #ff6b35;
      font-size: 15px;
      font-weight: bold;
      margin-bottom: 6px;
    }}
    .context {{
      color: #888;
      font-size: 13px;
      font-family: 'Courier New', monospace;
    }}
    .footer {{
      padding: 20px 36px;
      border-top: 1px solid #2a2a2a;
      color: #444;
      font-size: 11px;
      font-family: 'Courier New', monospace;
      letter-spacing: 1px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="label">Good morning</div>
      <div class="date">{today}</div>
    </div>
    <div class="body">
      <div class="quote">"{quote}"</div>
      <div class="attribution">— {source}</div>
      <div class="context">{context}</div>
    </div>
    <div class="footer">YOUR DAILY FUEL &nbsp;·&nbsp; 10:00 AM KST</div>
  </div>
</body>
</html>
"""


def send_email(quote_data: dict):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    today = datetime.now().strftime("%A, %b %d")
    subject = f"Morning fuel ⚡ {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient

    plain = f'"{quote_data["quote"]}"\n\n— {quote_data["source"]}\n{quote_data["context"]}'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(build_email_html(**quote_data), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Sent to {recipient}: {quote_data['source']}")


if __name__ == "__main__":
    quote_data = generate_quote()
    send_email(quote_data)
