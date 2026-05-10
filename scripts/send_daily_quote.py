import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def generate_quote() -> tuple[str, str]:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": """Give me one powerful, aspirational, inspirational quote that will make someone feel pumped, fired up, and absolutely ready to attack the day.

Draw from the full universe of human expression — movies, novels, speeches, interviews, songs, podcasts, letters, poems, locker room talks, anything. Be creative and diverse; don't always reach for the same famous figures. Dig for gems that feel alive.

Respond with ONLY these two lines, nothing else:
QUOTE: [the exact quote]
SOURCE: [who said/wrote it and the original context, e.g. "Rocky Balboa, Rocky Balboa (2006)" or "Kobe Bryant, interview with ESPN (2012)" or "Toni Morrison, Beloved (1987)" or "Lin-Manuel Miranda, Hamilton (2015)"]""",
            }
        ],
    )

    raw = message.content[0].text.strip()
    quote = ""
    source = ""
    for line in raw.splitlines():
        if line.startswith("QUOTE:"):
            quote = line.removeprefix("QUOTE:").strip()
        elif line.startswith("SOURCE:"):
            source = line.removeprefix("SOURCE:").strip()

    return quote, source


def build_html(quote: str, source: str) -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#0f0f0f;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0f0f0f;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" style="background:linear-gradient(145deg,#1a1a1a,#111);border-radius:16px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,0.6);">

          <!-- Top accent bar -->
          <tr>
            <td style="height:4px;background:linear-gradient(90deg,#f5a623,#f76b1c,#ff3b55);"></td>
          </tr>

          <!-- Header -->
          <tr>
            <td style="padding:36px 48px 0 48px;text-align:center;">
              <p style="margin:0;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#555;">Good Morning &bull; {today}</p>
              <h1 style="margin:16px 0 0 0;font-size:13px;letter-spacing:4px;text-transform:uppercase;color:#f5a623;font-weight:normal;">Your Daily Fuel</h1>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:24px 48px;">
              <hr style="border:none;border-top:1px solid #2a2a2a;">
            </td>
          </tr>

          <!-- Quote -->
          <tr>
            <td style="padding:0 48px 8px 48px;">
              <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="width:4px;background:linear-gradient(180deg,#f5a623,#f76b1c);border-radius:2px;"></td>
                  <td style="padding:4px 0 4px 24px;">
                    <p style="margin:0;font-size:24px;line-height:1.65;color:#f0ece4;font-style:italic;font-weight:normal;">&#8220;{quote}&#8221;</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Attribution -->
          <tr>
            <td style="padding:24px 48px 0 48px;text-align:right;">
              <p style="margin:0;font-size:14px;color:#888;font-style:normal;">&#8212;&nbsp;{source}</p>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:32px 48px 24px 48px;">
              <hr style="border:none;border-top:1px solid #2a2a2a;">
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:0 48px 40px 48px;text-align:center;">
              <p style="margin:0;font-size:16px;letter-spacing:2px;color:#f5a623;font-style:normal;">Go get it. Today is yours.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_email(quote: str, source: str) -> None:
    recipient = os.environ["RECIPIENT_EMAIL"]
    sender = os.environ["SMTP_EMAIL"]
    password = os.environ["SMTP_PASSWORD"]

    today = datetime.now().strftime("%B %d")
    subject = f"Morning Fuel — {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Morning Fuel <{sender}>"
    msg["To"] = recipient

    plain = f'"{quote}"\n\n— {source}\n\nGo get it. Today is yours.'
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(build_html(quote, source), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Sent to {recipient}")
    print(f'Quote: "{quote}"')
    print(f"Source: {source}")


if __name__ == "__main__":
    print("Generating quote...")
    quote, source = generate_quote()
    print(f"Quote generated. Sending email...")
    send_email(quote, source)
    print("Done.")
