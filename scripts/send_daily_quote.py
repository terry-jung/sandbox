#!/usr/bin/env python3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import anthropic

RECIPIENT = "thjung91@gmail.com"
SENDER = os.environ["GMAIL_USER"]
APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": (
                "Give me one powerful, aspirational, energizing quote to start the day. "
                "The quote can be from any source: a movie, book, speech, interview, song, podcast, conversation — anything. "
                "Pick something that feels alive and punchy, not overused or clichéd. "
                "Vary the source each time (fiction, sports, philosophy, music, film, science, history, etc.). "
                "Format your response exactly like this — nothing else:\n\n"
                "QUOTE: <the quote>\n"
                "SOURCE: <who said/wrote it and where it's from>"
            ),
        }
    ],
)

raw = message.content[0].text.strip()

quote = ""
source = ""
for line in raw.splitlines():
    if line.startswith("QUOTE:"):
        quote = line[len("QUOTE:"):].strip()
    elif line.startswith("SOURCE:"):
        source = line[len("SOURCE:"):].strip()

html_body = f"""
<html>
<body style="font-family: Georgia, serif; background: #fafafa; padding: 40px;">
  <div style="max-width: 600px; margin: auto; background: white; border-radius: 12px;
              padding: 48px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
    <p style="font-size: 13px; color: #999; text-transform: uppercase;
              letter-spacing: 2px; margin-bottom: 32px;">Good morning ☀️</p>
    <blockquote style="font-size: 22px; line-height: 1.6; color: #1a1a1a;
                       border-left: 4px solid #f0a500; padding-left: 24px;
                       margin: 0 0 28px 0; font-style: italic;">
      "{quote}"
    </blockquote>
    <p style="font-size: 15px; color: #555; margin: 0;">— {source}</p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 36px 0 24px;">
    <p style="font-size: 12px; color: #bbb; margin: 0;">
      Your daily dose of fire. Go make it happen.
    </p>
  </div>
</body>
</html>
"""

plain_body = f'"{quote}"\n\n— {source}\n\nGo make it happen.'

msg = MIMEMultipart("alternative")
msg["Subject"] = f"Your Morning Fuel: {source.split(',')[0].split('(')[0].strip()}"
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg.attach(MIMEText(plain_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER, APP_PASSWORD)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())

print(f"Sent: {quote[:60]}...")
