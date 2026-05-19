#!/usr/bin/env python3
import anthropic
import os
import json
from datetime import datetime
import pytz

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

kst = pytz.timezone("Asia/Seoul")
today = datetime.now(kst).strftime("%A, %B %d, %Y")

message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=600,
    messages=[
        {
            "role": "user",
            "content": f"""Generate one unique, powerful, aspirational quote for today ({today}).

Requirements:
- Genuinely inspiring with strong pump-up energy — something that makes you want to get up and conquer the day
- Can be from ANYWHERE: a movie, book, speech, article, interview, conversation, song, podcast, anime, TV show, game, or any source
- Include the exact quote, the person's name, and the source context
- Be creative and varied — think athletes, entrepreneurs, fictional heroes, musicians, scientists, activists, coaches, philosophers, comedians
- Avoid the most overused quotes (no "stay hungry stay foolish", no "be the change", no "just do it" as a standalone)
- Pick something that feels fresh, specific, and powerful

Respond ONLY with valid JSON in exactly this format:
{{"quote": "the exact quote text", "author": "Person Name", "source": "Source title and context (e.g. Rocky Balboa, Rocky IV, 1985)"}}""",
        }
    ],
)

data = json.loads(message.content[0].text)
quote = data["quote"]
author = data["author"]
source = data["source"]

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#f4f1eb;font-family:Georgia,'Times New Roman',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f1eb;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 30px rgba(0,0,0,0.08);">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);padding:40px 50px 30px;">
              <p style="margin:0;color:#e8c87a;font-size:11px;text-transform:uppercase;letter-spacing:4px;font-family:Arial,sans-serif;">Good Morning — {today}</p>
              <p style="margin:10px 0 0;color:#ffffff;font-size:28px;font-weight:bold;font-family:Arial,sans-serif;">Daily Ignition 🔥</p>
            </td>
          </tr>

          <!-- Quote -->
          <tr>
            <td style="padding:50px 50px 30px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="border-left:5px solid #e8c87a;padding-left:25px;">
                    <p style="margin:0;font-size:22px;line-height:1.65;color:#1a1a1a;font-style:italic;">"{quote}"</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Attribution -->
          <tr>
            <td style="padding:0 50px 50px;">
              <p style="margin:0;font-size:17px;color:#1a1a2e;font-weight:bold;font-family:Arial,sans-serif;">— {author}</p>
              <p style="margin:6px 0 0;font-size:13px;color:#888;font-family:Arial,sans-serif;font-style:italic;">{source}</p>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:0 50px;">
              <hr style="border:none;border-top:1px solid #eee;margin:0;">
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:30px 50px 40px;text-align:center;">
              <p style="margin:0;font-size:15px;color:#555;font-family:Arial,sans-serif;">Today is yours. Go take it. 💪</p>
              <p style="margin:12px 0 0;font-size:11px;color:#bbb;font-family:Arial,sans-serif;">Delivered every morning at 10am KST</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

github_output = os.environ.get("GITHUB_OUTPUT", "")
if github_output:
    with open(github_output, "a") as f:
        f.write(f"author={author}\n")
        f.write(f"quote_preview={quote[:80]}...\n")
        f.write(f"html<<QUOTE_EOF\n{html}\nQUOTE_EOF\n")

print(f"Quote: {quote}")
print(f"Author: {author}")
print(f"Source: {source}")
