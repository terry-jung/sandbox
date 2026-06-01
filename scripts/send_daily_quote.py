import anthropic
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def get_quote() -> tuple[str, str]:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "Give me one powerful, aspirational, and inspiring quote that will make "
                    "someone feel pumped and fired up to take on the day.\n\n"
                    "The quote can come from absolutely anywhere — a movie, book, speech, "
                    "article, interview, conversation, song, podcast, TV show, or anywhere else. "
                    "Mix it up: sometimes legendary athletes, sometimes philosophers, sometimes "
                    "fictional characters, sometimes musicians, sometimes entrepreneurs, sometimes "
                    "historical figures. Themes can include resilience, ambition, courage, "
                    "discipline, joy, growth, or just raw motivation.\n\n"
                    "Format your response EXACTLY like this — nothing else, no extra commentary:\n"
                    "QUOTE: [the quote]\n"
                    "SOURCE: [who said it / where it's from]"
                ),
            }
        ],
    )

    response = message.content[0].text.strip()
    quote, source = "", ""

    for line in response.splitlines():
        if line.startswith("QUOTE:"):
            quote = line.removeprefix("QUOTE:").strip()
        elif line.startswith("SOURCE:"):
            source = line.removeprefix("SOURCE:").strip()

    if not quote or not source:
        raise ValueError(f"Unexpected response format:\n{response}")

    return quote, source


def send_email(quote: str, source: str) -> None:
    gmail_address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ.get("RECIPIENT_EMAIL") or gmail_address

    today = datetime.now().strftime("%A, %B %d, %Y")

    html_body = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background-color:#f5f4f0;font-family:Georgia,serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f4f0;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:14px;padding:48px 44px;box-shadow:0 3px 16px rgba(0,0,0,0.07);">
          <tr>
            <td>
              <p style="margin:0 0 6px;color:#b0a898;font-size:11px;text-transform:uppercase;letter-spacing:3px;font-family:Arial,sans-serif;">
                Good Morning &nbsp;·&nbsp; {today}
              </p>
              <p style="margin:0 0 32px;color:#c8b99a;font-size:11px;text-transform:uppercase;letter-spacing:3px;font-family:Arial,sans-serif;">
                10:00 AM KST
              </p>

              <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td style="border-left:4px solid #1a1a1a;padding-left:22px;">
                    <p style="margin:0;font-size:23px;line-height:1.65;color:#111111;font-style:italic;">
                      &ldquo;{quote}&rdquo;
                    </p>
                  </td>
                </tr>
              </table>

              <p style="margin:24px 0 0;color:#555555;font-size:15px;font-family:Arial,sans-serif;">
                &mdash; {source}
              </p>

              <hr style="border:none;border-top:1px solid #eeece8;margin:36px 0 20px;">

              <p style="margin:0;color:#c8c4bc;font-size:11px;text-align:center;font-family:Arial,sans-serif;">
                Your daily spark &nbsp;&#9679;&nbsp; Go get it.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Good morning — your quote for {today}"
    msg["From"] = gmail_address
    msg["To"] = recipient
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, app_password)
        server.sendmail(gmail_address, recipient, msg.as_string())

    print(f"Sent to {recipient}")
    print(f'Quote: "{quote}"')
    print(f"Source: {source}")


if __name__ == "__main__":
    quote, source = get_quote()
    send_email(quote, source)
