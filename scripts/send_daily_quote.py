#!/usr/bin/env python3
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import anthropic

RECIPIENT_EMAIL = "thjung91@gmail.com"
SENDER_EMAIL = "thjung91@gmail.com"


def generate_quote() -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "Give me one aspirational, inspirational, positive quote that will help someone "
                    "feel pumped and ready to conquer their day. Pick something that genuinely moves "
                    "you — it can be from absolutely anywhere: a movie, a novel, a speech, an article, "
                    "an interview, a conversation, a song lyric, a podcast, a TV show, a comic, "
                    "social media, anywhere. Vary the source each time — don't always pick famous speeches. "
                    "Return ONLY the following two lines, nothing else:\n"
                    "QUOTE: <the exact quote>\n"
                    "SOURCE: <who said it and/or where it's from>"
                ),
            }
        ],
    )

    return message.content[0].text.strip()


def parse_quote(raw: str) -> tuple[str, str]:
    lines = raw.strip().splitlines()
    quote = ""
    source = ""
    for line in lines:
        if line.upper().startswith("QUOTE:"):
            quote = line.split(":", 1)[1].strip().strip('"')
        elif line.upper().startswith("SOURCE:"):
            source = line.split(":", 1)[1].strip()
    return quote, source


def build_email(quote: str, source: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Morning Boost ☀️"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    plain = f'"{quote}"\n\n— {source}\n\nHave an incredible day. Go get it.'

    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f0f0f;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f0f;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#1a1a1a;border-radius:12px;overflow:hidden;">
          <tr>
            <td style="background:linear-gradient(135deg,#ff6b35,#f7c59f);padding:6px 0;"></td>
          </tr>
          <tr>
            <td style="padding:48px 40px 32px;">
              <p style="margin:0 0 24px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#ff6b35;font-family:'Helvetica Neue',sans-serif;">
                Good morning &mdash; let&rsquo;s go
              </p>
              <blockquote style="margin:0 0 32px;padding:0 0 0 20px;border-left:3px solid #ff6b35;">
                <p style="margin:0;font-size:22px;line-height:1.6;color:#f0ede8;font-style:italic;">
                  &ldquo;{quote}&rdquo;
                </p>
              </blockquote>
              <p style="margin:0 0 40px;font-size:14px;color:#999;font-family:'Helvetica Neue',sans-serif;letter-spacing:1px;">
                &mdash; {source}
              </p>
              <p style="margin:0;font-size:15px;color:#ccc;font-family:'Helvetica Neue',sans-serif;">
                Have an incredible day. <strong style="color:#ff6b35;">Go get it.</strong>
              </p>
            </td>
          </tr>
          <tr>
            <td style="background:linear-gradient(135deg,#ff6b35,#f7c59f);padding:6px 0;"></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))
    return msg


def send_email(msg: MIMEMultipart) -> None:
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, app_password)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())


def main() -> None:
    raw = generate_quote()
    quote, source = parse_quote(raw)

    if not quote or not source:
        print(f"Failed to parse quote response:\n{raw}", file=sys.stderr)
        sys.exit(1)

    print(f'Quote: "{quote}"\nSource: {source}')

    msg = build_email(quote, source)
    send_email(msg)
    print("Email sent successfully.")


if __name__ == "__main__":
    main()
