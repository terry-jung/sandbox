#!/usr/bin/env python3
"""Generate an inspirational quote via Claude and email it."""

import os
import smtplib
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import anthropic

RECIPIENT = "thjung91@gmail.com"
SENDER    = "thjung91@gmail.com"

PROMPT = """\
Give me ONE short, powerful, aspirational quote that will make someone feel \
pumped and ready to conquer their day. It can be from a movie, book, speech, \
article, interview, conversation, song, or any source — real or fictional, \
ancient or modern. Be creative and varied; avoid clichés and overused quotes.

Reply with EXACTLY this format and nothing else:

QUOTE: "The quote text here."
SOURCE: Person/character name, Origin (e.g. film title, book, speech name, album)"""


def get_quote() -> tuple[str, str]:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=256,
        messages=[{"role": "user", "content": PROMPT}],
    )
    output = message.content[0].text.strip()
    quote, source = "", ""
    for line in output.splitlines():
        if line.startswith("QUOTE:"):
            quote = line[len("QUOTE:"):].strip().strip('"')
        elif line.startswith("SOURCE:"):
            source = line[len("SOURCE:"):].strip()
    if not quote:
        raise ValueError(f"Unexpected response format:\n{output}")
    return quote, source


def send_email(quote: str, source: str):
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    today = date.today().strftime("%A, %B %-d")
    subject = f"Your morning fuel — {today}"

    html = f"""\
<html>
<body style="font-family:Georgia,serif;max-width:580px;margin:48px auto;color:#1a1a1a;padding:0 24px;">
  <p style="font-size:12px;color:#aaa;margin-bottom:36px;letter-spacing:0.08em;text-transform:uppercase;">
    {today}
  </p>
  <blockquote style="border-left:4px solid #e63946;margin:0;padding:0 0 0 28px;">
    <p style="font-size:22px;line-height:1.6;font-style:italic;margin:0 0 20px 0;">
      &ldquo;{quote}&rdquo;
    </p>
    <p style="font-size:14px;color:#666;margin:0;">
      &mdash; {source}
    </p>
  </blockquote>
  <p style="font-size:20px;margin-top:48px;">Go get it. 🔥</p>
</body>
</html>"""

    plain = f'"{quote}"\n\n— {source}\n\nGo get it.'

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, app_password)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())

    print(f"Sent: \"{quote}\" — {source}")


if __name__ == "__main__":
    quote, source = get_quote()
    send_email(quote, source)
