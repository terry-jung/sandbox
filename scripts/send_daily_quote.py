import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date


def generate_quote():
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": """Give me one aspirational, inspirational, positive quote that will make someone feel pumped and ready to take on the day.

The quote can be from a movie, book, speech, article, interview, conversation, song, podcast, or any other source. Choose something genuinely powerful and motivating. Vary the source type each time — don't always pick famous speeches.

Format your response EXACTLY like this (nothing else):
QUOTE: [the quote text]
SOURCE: [who said it / where it's from]
CONTEXT: [one sentence about why this quote hits different]"""
        }]
    )
    return message.content[0].text


def send_email(quote_content):
    to_email = os.environ["TO_EMAIL"]
    from_email = os.environ["FROM_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    today = date.today().strftime("%B %d, %Y")

    quote = source = context = ""
    for line in quote_content.strip().split("\n"):
        if line.startswith("QUOTE:"):
            quote = line.replace("QUOTE:", "").strip()
        elif line.startswith("SOURCE:"):
            source = line.replace("SOURCE:", "").strip()
        elif line.startswith("CONTEXT:"):
            context = line.replace("CONTEXT:", "").strip()

    html = f"""
    <html>
    <body style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
        <div style="background-color: white; border-radius: 12px; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <p style="color: #888; font-size: 14px; margin-bottom: 30px;">Good morning &#9728;&#65039; &mdash; {today}</p>
            <div style="border-left: 4px solid #2c7be5; padding-left: 20px; margin: 30px 0;">
                <p style="font-size: 22px; line-height: 1.6; color: #1a1a2e; font-style: italic; margin: 0;">&ldquo;{quote}&rdquo;</p>
            </div>
            <p style="color: #444; font-size: 16px; font-weight: bold; margin-top: 20px;">&mdash; {source}</p>
            <p style="color: #666; font-size: 14px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">{context}</p>
            <p style="color: #aaa; font-size: 12px; margin-top: 30px;">Now go make today count. &#128170;</p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Morning Quote — {today}"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())

    print(f"Quote sent successfully to {to_email}")


if __name__ == "__main__":
    print("Generating today's quote...")
    quote_content = generate_quote()
    print(f"Generated:\n{quote_content}")
    send_email(quote_content)
