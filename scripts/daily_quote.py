import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

RECIPIENT_EMAIL = "thjung91@gmail.com"
SENDER_EMAIL = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

SYSTEM_PROMPT = """You are a curator of the most powerful, soul-stirring quotes ever spoken or written.
Your job is to select ONE quote that will make someone feel genuinely pumped, inspired, and ready to attack the day.

Rules:
- The quote must feel ALIVE — visceral, urgent, specific. Not generic platitudes.
- Pull from anywhere: movies, books, speeches, interviews, songs, podcasts, athletes, artists, scientists, fictional characters, philosophers, comedians, entrepreneurs — anything goes.
- Vary the source dramatically each time. Don't default to the usual suspects.
- The quote should feel like it was written for TODAY specifically.
- Include: the exact quote, the person/character who said it, and the context (movie title, book, speech occasion, etc.).
- Keep attribution tight and accurate."""

USER_PROMPT = """Give me one powerful, aspirational quote to start the day fired up.

Format your response EXACTLY like this:
QUOTE: [the quote]
FROM: [Name]
CONTEXT: [where it's from — e.g., "from the film Interstellar (2014)", "acceptance speech at the 1993 Oscars", "his book 'Man's Search for Meaning'", etc.]
PUMP: [one sentence on WHY this quote hits so hard right now]

No preamble, no commentary outside the format."""

def get_quote() -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        messages=[{"role": "user", "content": USER_PROMPT}],
        system=SYSTEM_PROMPT,
    )
    raw = message.content[0].text.strip()

    result = {}
    for line in raw.split("\n"):
        if line.startswith("QUOTE:"):
            result["quote"] = line.replace("QUOTE:", "").strip()
        elif line.startswith("FROM:"):
            result["from"] = line.replace("FROM:", "").strip()
        elif line.startswith("CONTEXT:"):
            result["context"] = line.replace("CONTEXT:", "").strip()
        elif line.startswith("PUMP:"):
            result["pump"] = line.replace("PUMP:", "").strip()
    return result


def build_email_html(q: dict) -> str:
    today = datetime.now().strftime("%A, %B %-d")
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#0a0a0a;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a0a;padding:40px 20px;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

        <!-- Header -->
        <tr><td style="padding-bottom:32px;text-align:center;">
          <p style="margin:0;font-family:'Arial',sans-serif;font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#666;">
            {today} &nbsp;·&nbsp; Good morning
          </p>
        </td></tr>

        <!-- Quote card -->
        <tr><td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);border-radius:16px;padding:48px 40px;">

          <!-- Opening mark -->
          <p style="margin:0 0 20px 0;font-size:72px;line-height:1;color:#e94560;font-family:'Georgia',serif;">&ldquo;</p>

          <!-- The quote -->
          <p style="margin:0 0 32px 0;font-size:22px;line-height:1.6;color:#f0f0f0;font-style:italic;font-family:'Georgia',serif;">
            {q.get('quote', '')}
          </p>

          <!-- Attribution -->
          <div style="border-left:3px solid #e94560;padding-left:20px;margin-bottom:28px;">
            <p style="margin:0 0 4px 0;font-size:16px;font-weight:bold;color:#e94560;font-family:'Arial',sans-serif;letter-spacing:1px;">
              {q.get('from', '')}
            </p>
            <p style="margin:0;font-size:12px;color:#888;font-family:'Arial',sans-serif;letter-spacing:0.5px;font-style:italic;">
              {q.get('context', '')}
            </p>
          </div>

          <!-- Why it hits -->
          <div style="background:rgba(233,69,96,0.1);border-radius:8px;padding:16px 20px;">
            <p style="margin:0;font-size:13px;line-height:1.6;color:#ccc;font-family:'Arial',sans-serif;">
              <span style="color:#e94560;font-weight:bold;">Why this today →</span> {q.get('pump', '')}
            </p>
          </div>

        </td></tr>

        <!-- Footer -->
        <tr><td style="padding-top:28px;text-align:center;">
          <p style="margin:0;font-family:'Arial',sans-serif;font-size:11px;color:#444;letter-spacing:2px;text-transform:uppercase;">
            Go get it. &nbsp;🔥
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_email(q: dict):
    today = datetime.now().strftime("%B %-d")
    subject = f"Your morning fuel — {today} ☀️"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    plain = f'"{q.get("quote", "")}"\n\n— {q.get("from", "")}\n{q.get("context", "")}\n\nWhy this today: {q.get("pump", "")}'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(build_email_html(q), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    print(f"Sent: {subject}")


if __name__ == "__main__":
    quote = get_quote()
    print(f"Quote: {quote}")
    send_email(quote)
    print("Done.")
