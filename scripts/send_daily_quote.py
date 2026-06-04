import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

RECIPIENT_EMAIL = "thjung91@gmail.com"
SENDER_EMAIL = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]


def get_quote() -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%B %d, %Y")

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Give me ONE aspirational, pumped-up, energizing quote "
                    "that will make someone feel fired up and ready to take on the day. "
                    "It can be from a movie, book, speech, interview, song, podcast, conversation — anything. "
                    "Pick something that feels electric and alive, not generic. "
                    "Vary the source widely across days (athletes, fictional characters, philosophers, musicians, "
                    "entrepreneurs, scientists, coaches, poets, etc.).\n\n"
                    "Respond in this exact JSON format with no extra text:\n"
                    '{"quote": "...", "author": "...", "source": "..."}\n\n'
                    "source = where it came from (e.g. 'Rocky Balboa, Rocky IV', "
                    "'Kobe Bryant, interview with ESPN 2012', 'Kendrick Lamar, HUMBLE.', "
                    "'David Goggins, Can't Hurt Me', etc.)"
                ),
            }
        ],
    )

    import json
    raw = message.content[0].text.strip()
    data = json.loads(raw)
    return data


def build_email_html(quote: str, author: str, source: str) -> str:
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      margin: 0; padding: 0;
      background: #0f0f0f;
      font-family: 'Georgia', serif;
    }}
    .wrapper {{
      max-width: 600px;
      margin: 40px auto;
      background: #1a1a1a;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 30px rgba(0,0,0,0.5);
    }}
    .header {{
      background: linear-gradient(135deg, #ff6b00, #ff0080);
      padding: 28px 32px 20px;
    }}
    .header .label {{
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: rgba(255,255,255,0.8);
      font-family: 'Arial', sans-serif;
    }}
    .header .date {{
      font-size: 15px;
      color: #fff;
      margin-top: 4px;
      font-family: 'Arial', sans-serif;
      font-weight: 600;
    }}
    .body {{
      padding: 40px 36px 32px;
    }}
    .quote {{
      font-size: 26px;
      line-height: 1.5;
      color: #f0f0f0;
      font-style: italic;
      margin: 0 0 28px;
    }}
    .quote::before {{ content: '\\201C'; color: #ff6b00; font-size: 48px; line-height: 0; vertical-align: -18px; margin-right: 4px; }}
    .quote::after  {{ content: '\\201D'; color: #ff6b00; font-size: 48px; line-height: 0; vertical-align: -18px; margin-left: 4px; }}
    .attribution {{
      border-left: 3px solid #ff6b00;
      padding-left: 16px;
    }}
    .author {{
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      font-family: 'Arial', sans-serif;
      margin-bottom: 4px;
    }}
    .source {{
      font-size: 13px;
      color: #888;
      font-family: 'Arial', sans-serif;
      font-style: italic;
    }}
    .footer {{
      padding: 20px 36px;
      background: #111;
      font-size: 12px;
      color: #555;
      font-family: 'Arial', sans-serif;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="label">Your Morning Fuel</div>
      <div class="date">{today_str}</div>
    </div>
    <div class="body">
      <p class="quote">{quote}</p>
      <div class="attribution">
        <div class="author">{author}</div>
        <div class="source">{source}</div>
      </div>
    </div>
    <div class="footer">Go make today count. &#128293;</div>
  </div>
</body>
</html>
"""


def send_email(quote: str, author: str, source: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Morning Fuel — {datetime.now().strftime('%b %d')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    html = build_email_html(quote, author, source)
    plain = f'"{quote}"\n\n— {author}\n({source})'

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    print(f"Sent: {author} — {quote[:60]}...")


if __name__ == "__main__":
    data = get_quote()
    send_email(data["quote"], data["author"], data["source"])
