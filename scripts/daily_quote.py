import anthropic
import smtplib
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": (
                "Give me one aspirational, inspirational, positive quote to start the day "
                "feeling pumped and ready to go. It can be from absolutely anything — a movie, "
                "book, speech, article, interview, conversation, song, podcast, or any other source. "
                "Mix it up and surprise me; don't always default to the same well-known speakers. "
                "Return ONLY the quote in quotation marks, then on a new line the attribution "
                "(name and source if relevant). No intro, no commentary, no extra text."
            ),
        }
    ],
)

quote_text = message.content[0].text.strip()

today = datetime.now().strftime("%B %d, %Y")

html_body = f"""
<html>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.08);overflow:hidden;">
        <tr>
          <td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px 40px;text-align:center;">
            <p style="margin:0;color:rgba(255,255,255,0.85);font-size:13px;letter-spacing:2px;text-transform:uppercase;">Good Morning</p>
            <p style="margin:6px 0 0;color:#ffffff;font-size:15px;">{today}</p>
          </td>
        </tr>
        <tr>
          <td style="padding:50px 40px 40px;">
            <div style="font-size:48px;color:#667eea;line-height:1;margin-bottom:20px;">"</div>
            <div style="font-size:20px;line-height:1.7;color:#2d3748;white-space:pre-wrap;">{quote_text}</div>
          </td>
        </tr>
        <tr>
          <td style="padding:0 40px 40px;text-align:center;">
            <p style="margin:0;color:#a0aec0;font-size:12px;letter-spacing:1px;">GO GET IT TODAY</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""

sender_email = os.environ["SENDER_EMAIL"]
sender_password = os.environ["SENDER_APP_PASSWORD"]
recipient_email = os.environ["RECIPIENT_EMAIL"]

msg = MIMEMultipart("alternative")
msg["Subject"] = f"Morning Quote — {today}"
msg["From"] = f"Daily Quote <{sender_email}>"
msg["To"] = recipient_email
msg.attach(MIMEText(html_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())

print(f"Sent to {recipient_email}:\n\n{quote_text}")
