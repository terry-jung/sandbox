import anthropic
import smtplib
import os
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

KST = timezone(timedelta(hours=9))


def generate_quote():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now(KST).strftime("%A, %B %d, %Y")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Today is {today} (KST). Give me one powerful, aspirational, and genuinely moving quote to start the day with incredible energy.

The quote can come from ANYWHERE — a movie, song, book, speech, podcast, interview, article, TV show, conversation, poem, anything. Go beyond the obvious ones everyone has heard a hundred times. Surprise me.

Respond in EXACTLY this format, nothing else:
QUOTE: [the exact quote]
SOURCE: [who said/wrote/sang it and the specific source, e.g. "Maximus, Gladiator (2000)" or "Kendrick Lamar, 'HUMBLE.' (2017)" or "Brené Brown, Daring Greatly (2012)" or "Kobe Bryant, interview with Jim Gray (2016)"]

The quote should make someone want to jump out of their chair and attack the day. Vary the tone — sometimes raw and fierce, sometimes poetic, sometimes quietly profound.""",
            }
        ],
    )

    response = message.content[0].text.strip()
    quote, source = "", ""
    for line in response.split("\n"):
        if line.startswith("QUOTE:"):
            quote = line[6:].strip()
        elif line.startswith("SOURCE:"):
            source = line[7:].strip()

    return quote, source


def send_email(quote, source):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]
    today = datetime.now(KST).strftime("%A, %B %d")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Good morning — {today}"
    msg["From"] = f"Daily Quote <{gmail_user}>"
    msg["To"] = recipient

    # Escape any quotes in the content for safe HTML embedding
    safe_quote = quote.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_source = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_today = today.replace("&", "&amp;")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#080810;font-family:Georgia,'Times New Roman',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" bgcolor="#080810">
    <tr>
      <td align="center" style="padding:48px 16px;">
        <table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">
          <tr>
            <td style="background:linear-gradient(160deg,#111128 0%,#0d1b3e 60%,#0a2545 100%);border-radius:20px;padding:56px 44px;text-align:center;border:1px solid #1e2d50;">

              <p style="color:#e8a020;font-size:11px;letter-spacing:5px;text-transform:uppercase;margin:0 0 36px 0;font-family:Helvetica,Arial,sans-serif;">Good Morning &#9728;</p>

              <p style="color:#f0eeea;font-size:22px;line-height:1.75;font-style:italic;margin:0 0 36px 0;font-weight:400;">&ldquo;{safe_quote}&rdquo;</p>

              <div style="width:48px;height:1px;background:#e8a020;margin:0 auto 24px auto;opacity:0.7;"></div>

              <p style="color:#8890a8;font-size:13px;letter-spacing:0.5px;margin:0 0 48px 0;font-family:Helvetica,Arial,sans-serif;">— {safe_source}</p>

              <p style="color:#2e3550;font-size:11px;font-family:Helvetica,Arial,sans-serif;margin:0;letter-spacing:1px;text-transform:uppercase;">{safe_today} &middot; Make it count.</p>

            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    plain = f'"{quote}"\n\n— {source}\n\n{today}. Make it count.'

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Sent on {today} (KST)")
    print(f"Quote: {quote}")
    print(f"Source: {source}")


if __name__ == "__main__":
    quote, source = generate_quote()
    send_email(quote, source)
