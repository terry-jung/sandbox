import anthropic
import smtplib
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_quote() -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    today = datetime.now().strftime("%A, %B %d, %Y")

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Give me ONE single aspirational, "
                    "pumped-up, get-after-it quote to start the morning with fire. "
                    "It can be from absolutely anything — a movie, novel, speech, song, "
                    "podcast, interview, TV show, athlete, founder, philosopher, coach, "
                    "artist, anyone. Pick something that genuinely moves people. "
                    "Rotate widely across sources — don't default to the same handful of names. "
                    "Respond in this exact JSON format with no extra text:\n"
                    '{"quote": "...", "source": "...", "context": "..."}\n\n'
                    "where `source` is the person's name and `context` is a brief note on "
                    "where it's from (e.g. 'Rocky Balboa, Rocky IV (1985)' or "
                    "'Kobe Bryant, interview with Jay Williams, 2019')."
                ),
            }
        ],
    )

    import json
    raw = message.content[0].text.strip()
    # strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def build_email(quote_data: dict) -> tuple[str, str]:
    today = datetime.now().strftime("%A, %B %d")
    quote = quote_data["quote"]
    source = quote_data["source"]
    context = quote_data["context"]

    subject = f"Good morning — your quote for {today}"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Georgia, serif; background: #0d0d0d; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 600px; margin: 40px auto; background: #141414; border-radius: 12px; overflow: hidden; }}
    .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
               padding: 40px 40px 30px; text-align: center; }}
    .header h1 {{ color: #f0c040; font-size: 13px; letter-spacing: 4px; text-transform: uppercase;
                  margin: 0 0 6px; font-weight: 400; }}
    .header p {{ color: #888; font-size: 12px; margin: 0; letter-spacing: 1px; }}
    .body {{ padding: 48px 44px 40px; }}
    .quote {{ color: #f5f0e8; font-size: 22px; line-height: 1.65; font-style: italic;
              margin: 0 0 32px; border-left: 3px solid #f0c040; padding-left: 20px; }}
    .attribution {{ color: #f0c040; font-size: 13px; font-style: normal; font-weight: 600;
                    letter-spacing: 0.5px; margin-bottom: 4px; }}
    .context {{ color: #666; font-size: 12px; }}
    .footer {{ border-top: 1px solid #222; padding: 20px 44px; text-align: center; }}
    .footer p {{ color: #444; font-size: 11px; margin: 0; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>Morning Fuel</h1>
      <p>{datetime.now().strftime("%A, %B %d, %Y")}</p>
    </div>
    <div class="body">
      <div class="quote">"{quote}"</div>
      <div class="attribution">— {source}</div>
      <div class="context">{context}</div>
    </div>
    <div class="footer">
      <p>Go get it. Today is yours.</p>
    </div>
  </div>
</body>
</html>"""

    plain = f'"{quote}"\n\n— {source}\n{context}\n\nGo get it. Today is yours.'

    return subject, html, plain


def send_email(subject: str, html: str, plain: str) -> None:
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Morning Fuel <{gmail_user}>"
    msg["To"] = recipient

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Quote sent to {recipient}")


if __name__ == "__main__":
    quote_data = get_quote()
    print(f"Quote: {quote_data['quote'][:60]}...")
    subject, html, plain = build_email(quote_data)
    send_email(subject, html, plain)
