import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=600,
    messages=[
        {
            "role": "user",
            "content": (
                "Give me one aspirational, inspirational, and positive quote that will make someone "
                "feel genuinely pumped and ready to crush their day.\n\n"
                "Source variety matters — rotate broadly across: movies, books, speeches, songs, "
                "podcasts, interviews, TV shows, athletes, artists, scientists, entrepreneurs, "
                "fictional characters, historical figures, philosophers, coaches, and more. "
                "Include the lesser-known gems, not just the famous overused ones.\n\n"
                "Format your response EXACTLY like this (nothing else, no extra text):\n"
                "QUOTE: [the quote text]\n"
                "SOURCE: [who said it — name + context e.g. 'Rocky Balboa, Rocky Balboa (2006)']\n"
                "CONTEXT: [one punchy sentence on why this quote hits hard]"
            ),
        }
    ],
)

response = message.content[0].text.strip()
quote, source, context = "", "", ""

for line in response.split("\n"):
    if line.startswith("QUOTE:"):
        quote = line[6:].strip()
    elif line.startswith("SOURCE:"):
        source = line[7:].strip()
    elif line.startswith("CONTEXT:"):
        context = line[8:].strip()

kst_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
date_str = kst_now.strftime("%A, %B %d, %Y")

subject = f"Good morning ☀️ — {date_str}"

html_body = f"""
<html>
<body style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto;
             padding: 40px 20px; background-color: #f5f5f0;">
  <div style="background: white; border-radius: 14px; padding: 44px 40px;
              box-shadow: 0 4px 24px rgba(0,0,0,0.07);">

    <p style="color: #aaa; font-size: 13px; margin: 0 0 32px 0;
              text-transform: uppercase; letter-spacing: 2px;">
      {date_str}
    </p>

    <blockquote style="border-left: 5px solid #f5a623; padding-left: 24px;
                       margin: 0 0 24px 0;">
      <p style="font-size: 21px; line-height: 1.65; color: #111;
                font-style: italic; margin: 0;">
        &ldquo;{quote}&rdquo;
      </p>
    </blockquote>

    <p style="font-size: 15px; color: #333; font-weight: 700;
              margin: 0 0 10px 28px;">
      — {source}
    </p>

    <p style="font-size: 14px; color: #888; font-style: italic;
              margin: 0 0 0 28px; line-height: 1.5;">
      {context}
    </p>

    <hr style="border: none; border-top: 1px solid #eee; margin: 36px 0 24px 0;">

    <p style="font-size: 13px; color: #bbb; text-align: center; margin: 0;">
      Let&rsquo;s go. You&rsquo;ve got this. 💪
    </p>

  </div>
</body>
</html>
"""

sender = os.environ["SENDER_EMAIL"]
recipient = os.environ["RECIPIENT_EMAIL"]
password = os.environ["GMAIL_APP_PASSWORD"]

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = f"Morning Quote ☀️ <{sender}>"
msg["To"] = recipient
msg.attach(MIMEText(html_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.sendmail(sender, recipient, msg.as_string())

print(f"Sent: {quote[:60]}...")
print(f"Source: {source}")
