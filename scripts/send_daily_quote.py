import anthropic
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def generate_quote() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "Pick ONE aspirational, powerful, positive quote to start someone's morning feeling pumped and unstoppable. "
                    "Pull from anywhere — movies, books, speeches, interviews, songs, podcasts, anime, TV shows, athletes, artists, "
                    "scientists, entrepreneurs, philosophers, coaches, fictional characters. "
                    "Rotate widely; avoid the same tired quotes everyone already knows. "
                    "Be bold in your choices.\n\n"
                    "Respond in EXACTLY this format with no extra text:\n"
                    "QUOTE: [the exact quote]\n"
                    "SOURCE: [who said it and where it's from, e.g. 'Rocky Balboa, Rocky Balboa (2006)' or 'Kobe Bryant, interview with ESPN (2012)']\n"
                    "FUEL: [one punchy sentence on why this quote hits hard today]"
                ),
            }
        ],
    )
    return message.content[0].text


def parse_quote(raw: str) -> tuple[str, str, str]:
    quote = source = fuel = ""
    for line in raw.strip().splitlines():
        if line.startswith("QUOTE:"):
            quote = line[len("QUOTE:"):].strip()
        elif line.startswith("SOURCE:"):
            source = line[len("SOURCE:"):].strip()
        elif line.startswith("FUEL:"):
            fuel = line[len("FUEL:"):].strip()
    return quote, source, fuel


def build_html(quote: str, source: str, fuel: str) -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{ margin: 0; padding: 0; background: #0f0f0f; font-family: 'Georgia', serif; color: #f0f0f0; }}
    .container {{ max-width: 600px; margin: 40px auto; padding: 0 20px; }}
    .header {{ text-align: center; margin-bottom: 40px; }}
    .date {{ font-size: 13px; letter-spacing: 3px; text-transform: uppercase; color: #888; margin-bottom: 8px; }}
    .title {{ font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #c8a96e; }}
    .quote-block {{ background: linear-gradient(135deg, #1a1a1a, #222); border-left: 4px solid #c8a96e; padding: 36px 40px; border-radius: 4px; margin: 20px 0; }}
    .quote-mark {{ font-size: 80px; color: #c8a96e; opacity: 0.3; line-height: 0.6; margin-bottom: 16px; display: block; }}
    .quote-text {{ font-size: 22px; line-height: 1.6; color: #f5f5f5; font-style: italic; margin: 0 0 24px 0; }}
    .source {{ font-size: 14px; color: #c8a96e; letter-spacing: 1px; font-style: normal; }}
    .fuel {{ background: #1a1a1a; border-radius: 4px; padding: 20px 24px; margin-top: 20px; font-size: 15px; color: #ccc; line-height: 1.6; }}
    .fuel-label {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #c8a96e; margin-bottom: 8px; }}
    .footer {{ text-align: center; margin-top: 40px; font-size: 11px; color: #555; letter-spacing: 2px; text-transform: uppercase; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="date">{today}</div>
      <div class="title">Your Morning Fuel</div>
    </div>
    <div class="quote-block">
      <span class="quote-mark">&ldquo;</span>
      <p class="quote-text">{quote}</p>
      <div class="source">— {source}</div>
    </div>
    <div class="fuel">
      <div class="fuel-label">Why it hits</div>
      {fuel}
    </div>
    <div class="footer">Go get it. Today is yours.</div>
  </div>
</body>
</html>"""


def send_email(html_body: str, plain_quote: str, source: str) -> None:
    sender = os.environ["SENDER_EMAIL"]
    recipient = os.environ["RECIPIENT_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    today = datetime.now().strftime("%A, %b %d")
    subject = f"Morning Fuel — {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    plain = f'"{plain_quote}"\n\n— {source}\n\nGo get it. Today is yours.'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Sent: {subject}")


def main() -> None:
    print("Generating quote...")
    raw = generate_quote()
    print(f"Raw response:\n{raw}\n")

    quote, source, fuel = parse_quote(raw)
    if not quote or not source:
        print("Failed to parse quote", file=sys.stderr)
        sys.exit(1)

    html = build_html(quote, source, fuel)
    send_email(html, quote, source)


if __name__ == "__main__":
    main()
