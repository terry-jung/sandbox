import anthropic
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_quote():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": (
                    "Give me one aspirational, inspirational, positive quote that will help someone "
                    "feel pumped and ready to conquer their day. "
                    "The quote can be from a movie, book, speech, article, interview, conversation, "
                    "song, podcast, or any other source — mix it up each time.\n\n"
                    "Format your response exactly like this (no extra text):\n"
                    "QUOTE: [the quote text]\n"
                    "ATTRIBUTION: [person's name]\n"
                    "SOURCE: [where it's from, e.g. 'The Dark Knight (2008)', 'Shoe Dog', "
                    "'Stanford Commencement Speech 2005', 'Interview with Tim Ferriss']\n\n"
                    "Make it genuinely powerful and uplifting. Avoid overused clichés."
                ),
            }
        ],
    )
    return message.content[0].text


def parse_quote(raw):
    quote = attribution = source = ""
    for line in raw.strip().splitlines():
        if line.startswith("QUOTE:"):
            quote = line[len("QUOTE:"):].strip().strip('"').strip("“”")
        elif line.startswith("ATTRIBUTION:"):
            attribution = line[len("ATTRIBUTION:"):].strip()
        elif line.startswith("SOURCE:"):
            source = line[len("SOURCE:"):].strip()
    return quote, attribution, source


def send_email(quote, attribution, source, recipient, sender, app_password):
    today = datetime.now().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Morning Fuel — {today}"
    msg["From"] = sender
    msg["To"] = recipient

    plain = f'"{quote}"\n\n— {attribution}\n{source}\n\nHave an amazing day. You’ve got this. \U0001f4aa'

    html = f"""\
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f0f2f5;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:40px 20px;">
      <table width="600" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);border-radius:16px;overflow:hidden;">
        <tr>
          <td style="padding:48px 40px 32px;text-align:center;">
            <p style="color:rgba(255,255,255,0.5);font-size:12px;letter-spacing:3px;text-transform:uppercase;margin:0 0 32px;">Good morning ☀️ {today}</p>
            <blockquote style="color:#fff;font-size:24px;line-height:1.65;font-style:italic;margin:0 0 28px;padding:0;">
              &ldquo;{quote}&rdquo;
            </blockquote>
            <p style="color:#f0c040;font-size:16px;font-weight:bold;margin:0 0 6px;">&mdash; {attribution}</p>
            <p style="color:rgba(255,255,255,0.45);font-size:13px;margin:0;">{source}</p>
          </td>
        </tr>
        <tr>
          <td style="padding:24px 40px 40px;text-align:center;">
            <p style="color:rgba(255,255,255,0.35);font-size:13px;margin:0;">
              You’ve got this. Go make today count. \U0001f4aa
            </p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Sent to {recipient}: \"{quote}\" — {attribution}")


if __name__ == "__main__":
    recipient = os.environ.get("RECIPIENT_EMAIL", "thjung91@gmail.com")
    sender = os.environ["GMAIL_USER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    raw = get_quote()
    print("Raw response:\n", raw)
    quote, attribution, source = parse_quote(raw)
    send_email(quote, attribution, source, recipient, sender, app_password)
