import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": (
                "Give me one powerful, aspirational, and inspirational quote that will make someone "
                "feel genuinely pumped and ready to conquer their day.\n\n"
                "Draw from any source: movies, books, speeches, articles, interviews, conversations, "
                "songs, podcasts, TV shows, comedy specials, athletes, artists, entrepreneurs, "
                "philosophers, fictional characters — anything goes.\n\n"
                "Aim for quotes that are vivid, specific, and hit different — not the usual overused ones. "
                "Surprise me.\n\n"
                "Respond in EXACTLY this format, nothing else:\n"
                "QUOTE: [the exact quote]\n"
                "SOURCE: [who said/wrote it and where, e.g. 'Maximus, Gladiator (2000)' "
                "or 'Kobe Bryant, interview with GQ, 2015' or 'David Goggins, Can't Hurt Me']"
            ),
        }
    ],
)

response_text = message.content[0].text.strip()
quote = ""
source = ""
for line in response_text.split("\n"):
    if line.startswith("QUOTE:"):
        quote = line[6:].strip().strip('"')
    elif line.startswith("SOURCE:"):
        source = line[7:].strip()

today = datetime.now().strftime("%B %d, %Y")

html_body = f"""
<html>
<body style="font-family: Georgia, 'Times New Roman', serif; max-width: 600px; margin: 0 auto;
             padding: 40px 20px; background-color: #f5f5f0;">
  <div style="background: #ffffff; border-radius: 16px; padding: 50px 44px;
              box-shadow: 0 4px 24px rgba(0,0,0,0.07);">

    <p style="color: #999; font-size: 12px; text-transform: uppercase; letter-spacing: 3px;
              margin: 0 0 36px; font-family: 'Helvetica Neue', Arial, sans-serif;">
      Good morning &nbsp;·&nbsp; {today}
    </p>

    <blockquote style="border-left: 5px solid #1a1a1a; margin: 0; padding: 16px 28px;
                       font-size: 22px; line-height: 1.65; color: #111; font-style: italic;">
      &ldquo;{quote}&rdquo;
    </blockquote>

    <p style="color: #555; font-size: 15px; margin: 20px 0 0 28px;
              font-family: 'Helvetica Neue', Arial, sans-serif;">
      &mdash; {source}
    </p>

    <hr style="border: none; border-top: 1px solid #ececec; margin: 44px 0 24px;">

    <p style="color: #bbb; font-size: 12px; text-align: center; margin: 0;
              font-family: 'Helvetica Neue', Arial, sans-serif; letter-spacing: 1px;">
      Go get it. Today is yours.
    </p>

  </div>
</body>
</html>
"""

plain_body = f'Good morning — {today}\n\n"{quote}"\n\n— {source}\n\nGo get it. Today is yours.'

sender = os.environ["GMAIL_ADDRESS"]
recipient = os.environ["GMAIL_ADDRESS"]
app_password = os.environ["GMAIL_APP_PASSWORD"]

msg = MIMEMultipart("alternative")
msg["Subject"] = f"Morning Fuel — {today}"
msg["From"] = sender
msg["To"] = recipient
msg.attach(MIMEText(plain_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, app_password)
    server.sendmail(sender, recipient, msg.as_string())

print(f"Sent successfully!")
print(f'Quote: "{quote}"')
print(f"Source: {source}")
