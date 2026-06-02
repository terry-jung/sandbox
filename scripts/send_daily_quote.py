import anthropic
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def generate_quote():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now().strftime("%A, %B %d, %Y")

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""Today is {today}. Give me ONE aspirational, inspirational, powerful quote that will pump someone up and make them feel unstoppable and ready to conquer the day.

The quote can be from absolutely anywhere — a movie, book, speech, interview, song, podcast, conversation, article, TV show, anything. Be diverse: mix it up across historical figures, modern leaders, athletes, artists, musicians, fictional characters, coaches, entrepreneurs, philosophers, etc. Surprise me.

Respond in EXACTLY this format (three lines, nothing else):
QUOTE: [the quote text]
SOURCE: [who said it / where it's from — be specific, e.g. "Denzel Washington, 2011 Dillard University commencement speech" or "Rocky Balboa, Rocky Balboa (2006)"]
CONTEXT: [1 punchy sentence about why this quote hits hard or who said it]"""
        }]
    )

    return message.content[0].text


def parse_quote(text):
    quote = source = context = ""
    for line in text.strip().split("\n"):
        if line.startswith("QUOTE:"):
            quote = line[6:].strip()
        elif line.startswith("SOURCE:"):
            source = line[7:].strip()
        elif line.startswith("CONTEXT:"):
            context = line[8:].strip()
    return quote, source, context


def build_html(quote, source, context, today):
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      background-color: #f5f0ea;
      margin: 0;
      padding: 20px;
    }}
    .container {{
      max-width: 580px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }}
    .header {{
      background: linear-gradient(135deg, #ff5f1f 0%, #ff8c42 100%);
      padding: 36px 44px 28px;
    }}
    .header-label {{
      color: rgba(255,255,255,0.85);
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      font-family: Arial, sans-serif;
      margin: 0 0 6px;
    }}
    .header-date {{
      color: #ffffff;
      font-size: 26px;
      font-weight: bold;
      margin: 0;
      font-family: Arial, sans-serif;
    }}
    .body {{
      padding: 44px 44px 28px;
    }}
    .open-quote {{
      font-size: 72px;
      color: #ff5f1f;
      line-height: 0.6;
      margin-bottom: 18px;
      font-family: Georgia, serif;
      display: block;
    }}
    .quote-text {{
      font-size: 22px;
      line-height: 1.65;
      color: #111111;
      font-style: italic;
      margin: 0 0 32px;
    }}
    .divider {{
      width: 48px;
      height: 3px;
      background: linear-gradient(90deg, #ff5f1f, #ff8c42);
      border-radius: 2px;
      margin: 0 0 24px;
    }}
    .source {{
      font-size: 15px;
      font-weight: bold;
      color: #222;
      font-family: Arial, sans-serif;
      font-style: normal;
      margin: 0 0 8px;
    }}
    .context {{
      font-size: 13px;
      color: #888;
      font-style: normal;
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 0;
    }}
    .cta {{
      margin: 36px 44px 0;
      background: linear-gradient(135deg, #ff5f1f 0%, #ff8c42 100%);
      border-radius: 10px;
      padding: 18px 24px;
      text-align: center;
    }}
    .cta-text {{
      color: #ffffff;
      font-size: 14px;
      font-weight: bold;
      letter-spacing: 2px;
      font-family: Arial, sans-serif;
      margin: 0;
    }}
    .footer {{
      padding: 24px 44px;
      text-align: center;
      font-size: 12px;
      color: #bbb;
      font-family: Arial, sans-serif;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <p class="header-label">Good Morning ☀️</p>
      <p class="header-date">{today}</p>
    </div>
    <div class="body">
      <span class="open-quote">"</span>
      <p class="quote-text">{quote}</p>
      <div class="divider"></div>
      <p class="source">— {source}</p>
      <p class="context">{context}</p>
    </div>
    <div class="cta">
      <p class="cta-text">TODAY IS YOUR DAY. GO GET IT. 🔥</p>
    </div>
    <div class="footer">
      Your daily dose of inspiration • Every morning at 10am KST
    </div>
  </div>
</body>
</html>"""


def send_email(quote, source, context):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ.get("RECIPIENT_EMAIL", gmail_user)

    today = datetime.now().strftime("%A, %B %d")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"☀️ Morning Fuel — {today}"
    msg["From"] = gmail_user
    msg["To"] = recipient

    plain = f"""Good Morning! {today}

"{quote}"

— {source}

{context}

TODAY IS YOUR DAY. GO GET IT. 🔥
"""

    html = build_html(quote, source, context, today)

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Sent to {recipient}")
    print(f'Quote: "{quote}"')
    print(f"Source: {source}")


if __name__ == "__main__":
    print("Generating quote...")
    raw = generate_quote()
    print(f"Raw output:\n{raw}\n")

    quote, source, context = parse_quote(raw)

    if not quote or not source:
        print("Failed to parse quote. Raw output above.")
        sys.exit(1)

    send_email(quote, source, context)
    print("Done!")
