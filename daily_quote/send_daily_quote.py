#!/usr/bin/env python3
"""
Daily Inspirational Quote Emailer
Sends a curated quote every morning to thjung91@gmail.com
"""

import smtplib
import ssl
import os
import sys
import hashlib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

RECIPIENT = "thjung91@gmail.com"
SENDER = "thjung91@gmail.com"
SUBJECT_PREFIX = "Your Morning Quote"

# Gmail SMTP config
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

# Load app password from env or file
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
if not APP_PASSWORD:
    cfg_path = os.path.join(os.path.dirname(__file__), ".gmail_app_password")
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            APP_PASSWORD = f.read().strip()

# ------------------------------------------------------------
# QUOTES — varied sources: movies, books, speeches, songs,
#          interviews, conversations, and more.
# ------------------------------------------------------------
QUOTES = [
    # Action / Drive
    ("The cave you fear to enter holds the treasure you seek.",
     "Joseph Campbell, 'The Hero with a Thousand Faces' (1949)"),

    ("You miss 100% of the shots you don't take.",
     "Wayne Gretzky"),

    ("It always seems impossible until it's done.",
     "Nelson Mandela"),

    ("Don't count the days. Make the days count.",
     "Muhammad Ali"),

    ("The secret of getting ahead is getting started.",
     "Mark Twain"),

    ("Hard work beats talent when talent doesn't work hard.",
     "Tim Notke, basketball coach"),

    ("You've got to get up every morning with determination if you're going to go to bed with satisfaction.",
     "George Lorimer"),

    ("Do something today that your future self will thank you for.",
     "Sean Patrick Flanery"),

    ("The only way to do great work is to love what you do.",
     "Steve Jobs, Stanford commencement address (2005)"),

    ("Push yourself, because no one else is going to do it for you.",
     "Unknown"),

    # Resilience / Grit
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.",
     "Winston Churchill"),

    ("It does not matter how slowly you go as long as you do not stop.",
     "Confucius"),

    ("Fall seven times, stand up eight.",
     "Japanese proverb"),

    ("I am not afraid of storms, for I am learning how to sail my ship.",
     "Louisa May Alcott, 'Little Women' (1868)"),

    ("The world breaks everyone, and afterward, some are strong at the broken places.",
     "Ernest Hemingway, 'A Farewell to Arms' (1929)"),

    ("When you come to the end of your rope, tie a knot and hang on.",
     "Franklin D. Roosevelt"),

    ("Tough times never last, but tough people do.",
     "Robert H. Schuller"),

    ("Out of difficulties grow miracles.",
     "Jean de la Bruyère"),

    ("Rock bottom became the solid foundation on which I rebuilt my life.",
     "J.K. Rowling, Harvard commencement address (2008)"),

    ("Scars show us where we have been, they do not dictate where we are going.",
     "David Rossi, Criminal Minds"),

    # Belief in Yourself
    ("Believe you can and you're halfway there.",
     "Theodore Roosevelt"),

    ("You are braver than you believe, stronger than you seem, and smarter than you think.",
     "A.A. Milne, 'Winnie-the-Pooh' (1926)"),

    ("Whether you think you can, or you think you can't — you're right.",
     "Henry Ford"),

    ("To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
     "Ralph Waldo Emerson"),

    ("No one can make you feel inferior without your consent.",
     "Eleanor Roosevelt, 'This Is My Story' (1937)"),

    ("You have power over your mind — not outside events. Realize this, and you will find strength.",
     "Marcus Aurelius, 'Meditations'"),

    ("I can't go back to yesterday because I was a different person then.",
     "Lewis Carroll, 'Alice's Adventures in Wonderland' (1865)"),

    ("Act as if what you do makes a difference. It does.",
     "William James"),

    ("Everything you've ever wanted is on the other side of fear.",
     "George Addair"),

    ("You are the author of your own story.",
     "Unknown"),

    # Purpose / Meaning
    ("The two most important days in your life are the day you are born and the day you find out why.",
     "Mark Twain"),

    ("The purpose of life is to live it, to taste experience to the utmost, to reach out eagerly and without fear for newer and richer experience.",
     "Eleanor Roosevelt"),

    ("He who has a why to live can bear almost any how.",
     "Friedrich Nietzsche"),

    ("The meaning of life is to find your gift. The purpose of life is to give it away.",
     "Pablo Picasso"),

    ("To live is the rarest thing in the world. Most people exist, that is all.",
     "Oscar Wilde"),

    ("In the middle of difficulty lies opportunity.",
     "Albert Einstein"),

    ("Life is either a daring adventure or nothing at all.",
     "Helen Keller, 'The Open Door' (1957)"),

    ("The purpose of our lives is to be happy.",
     "Dalai Lama XIV"),

    ("Don't ask what the world needs. Ask what makes you come alive, and go do it. Because what the world needs is people who have come alive.",
     "Howard Thurman"),

    # Excellence / Craft
    ("Excellence is not a destination; it is a continuous journey that never ends.",
     "Brian Tracy"),

    ("Whatever you are, be a good one.",
     "Abraham Lincoln"),

    ("I am not a product of my circumstances. I am a product of my decisions.",
     "Stephen Covey, 'The 7 Habits of Highly Effective People'"),

    ("We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
     "Will Durant, summarizing Aristotle"),

    ("Perfection is not attainable, but if we chase perfection we can catch excellence.",
     "Vince Lombardi"),

    ("If you're going through hell, keep going.",
     "Winston Churchill"),

    ("Make each day your masterpiece.",
     "John Wooden"),

    ("The difference between ordinary and extraordinary is that little extra.",
     "Jimmy Johnson"),

    # Movies & TV
    ("Why do we fall? So that we can learn to pick ourselves up.",
     "Alfred, 'Batman Begins' (2005)"),

    ("In my experience, there's no such thing as luck.",
     "Obi-Wan Kenobi, 'Star Wars: A New Hope' (1977)"),

    ("Life is like a box of chocolates — you never know what you're gonna get.",
     "Forrest Gump, 'Forrest Gump' (1994)"),

    ("Just keep swimming.",
     "Dory, 'Finding Nemo' (2003)"),

    ("The flower that blooms in adversity is the rarest and most beautiful of all.",
     "The Emperor, 'Mulan' (1998)"),

    ("To infinity and beyond!",
     "Buzz Lightyear, 'Toy Story' (1995)"),

    ("Oh yes, the past can hurt. But the way I see it, you can either run from it or learn from it.",
     "Rafiki, 'The Lion King' (1994)"),

    ("Get busy living, or get busy dying.",
     "Andy Dufresne, 'The Shawshank Redemption' (1994)"),

    ("Every passing minute is another chance to turn it all around.",
     "Sofia, 'Vanilla Sky' (2001)"),

    ("It's not about how hard you hit. It's about how hard you can get hit and keep moving forward.",
     "Rocky Balboa, 'Rocky Balboa' (2006)"),

    ("Happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
     "Albus Dumbledore, 'Harry Potter and the Prisoner of Azkaban' (film, 2004)"),

    ("Hope. It is the only thing stronger than fear.",
     "President Snow (ironically), 'The Hunger Games' (2012)"),

    ("What we do in life echoes in eternity.",
     "Maximus, 'Gladiator' (2000)"),

    ("You is kind, you is smart, you is important.",
     "Aibileen Clark, 'The Help' (2011)"),

    # Music / Songs
    ("You may say I'm a dreamer, but I'm not the only one.",
     "John Lennon, 'Imagine' (1971)"),

    ("Don't stop believin'. Hold on to that feeling.",
     "Journey, 'Don't Stop Believin'' (1981)"),

    ("Rise up, in spite of the ache.",
     "Andra Day, 'Rise Up' (2015)"),

    ("There ain't no mountain high enough to keep me from you.",
     "Marvin Gaye & Tammi Terrell, 'Ain't No Mountain High Enough' (1967)"),

    ("What doesn't kill you makes you stronger.",
     "Kelly Clarkson, 'Stronger' (2011)"),

    ("I will survive.",
     "Gloria Gaynor, 'I Will Survive' (1978)"),

    ("Keep your eyes on the stars, and your feet on the ground.",
     "Theodore Roosevelt"),

    ("I was born this way.",
     "Lady Gaga, 'Born This Way' (2011)"),

    ("Roar — I am a champion and you're gonna hear me.",
     "Katy Perry, 'Roar' (2013)"),

    # Speeches / Interviews
    ("We choose to go to the Moon — not because it is easy, but because it is hard.",
     "John F. Kennedy, Rice University speech (1962)"),

    ("We are the ones we have been waiting for.",
     "June Jordan, poem; made famous by Barack Obama (2008)"),

    ("The future belongs to those who believe in the beauty of their dreams.",
     "Eleanor Roosevelt"),

    ("There is no passion to be found playing small — in settling for a life that is less than the one you are capable of living.",
     "Nelson Mandela"),

    ("Our deepest fear is not that we are inadequate. Our deepest fear is that we are powerful beyond measure.",
     "Marianne Williamson, 'A Return to Love' (1992)"),

    ("I have a dream that one day this nation will rise up and live out the true meaning of its creed.",
     "Martin Luther King Jr., March on Washington speech (1963)"),

    ("Spread love everywhere you go.",
     "Mother Teresa"),

    ("The most courageous act is still to think for yourself. Aloud.",
     "Coco Chanel"),

    ("You don't have to be great to start, but you have to start to be great.",
     "Zig Ziglar"),

    ("I attribute my success to this: I never gave or took any excuse.",
     "Florence Nightingale"),

    # Growth & Learning
    ("The more that you read, the more things you will know. The more that you learn, the more places you'll go.",
     "Dr. Seuss, 'I Can Read With My Eyes Shut!' (1978)"),

    ("Every day is a new beginning. Take a deep breath, smile, and start again.",
     "Unknown"),

    ("An investment in knowledge pays the best interest.",
     "Benjamin Franklin"),

    ("Education is the most powerful weapon which you can use to change the world.",
     "Nelson Mandela"),

    ("Live as if you were to die tomorrow. Learn as if you were to live forever.",
     "Mahatma Gandhi"),

    ("Do not go where the path may lead, go instead where there is no path and leave a trail.",
     "Ralph Waldo Emerson"),

    ("The expert in anything was once a beginner.",
     "Helen Hayes"),

    ("It's not whether you get knocked down; it's whether you get up.",
     "Vince Lombardi"),

    # Attitude / Mindset
    ("Attitude is a little thing that makes a big difference.",
     "Winston Churchill"),

    ("The only disability in life is a bad attitude.",
     "Scott Hamilton"),

    ("Keep your face always toward the sunshine — and shadows will fall behind you.",
     "Walt Whitman"),

    ("Once you replace negative thoughts with positive ones, you'll start having positive results.",
     "Willie Nelson"),

    ("In every day, there are 1,440 minutes. That means we have 1,440 daily opportunities to make a positive impact.",
     "Les Brown"),

    ("Start each day with a grateful heart.",
     "Unknown"),

    ("Smile in the mirror. Do that every morning and you'll start to see a big difference in your life.",
     "Yoko Ono"),

    ("Optimism is the faith that leads to achievement.",
     "Helen Keller"),

    ("You cannot have a positive life and a negative mind.",
     "Joyce Meyer"),

    # Courage / Risk
    ("Security is mostly a superstition. Life is either a daring adventure or nothing.",
     "Helen Keller"),

    ("Courage is not the absence of fear, but the judgment that something else is more important than fear.",
     "Ambrose Redmoon"),

    ("The brave may not live forever, but the cautious do not live at all.",
     "Meg Cabot, 'The Princess Diaries' (2000)"),

    ("Do one thing every day that scares you.",
     "Mary Schmich, Chicago Tribune column (1997); often attributed to Eleanor Roosevelt"),

    ("You can't cross the sea merely by standing and staring at the water.",
     "Rabindranath Tagore"),

    ("A ship in harbor is safe — but that is not what ships are for.",
     "John A. Shedd"),

    ("And, when you want something, all the universe conspires in helping you to achieve it.",
     "Paulo Coelho, 'The Alchemist' (1988)"),

    ("Whatever you do, or dream you can, begin it. Boldness has genius, power, and magic in it.",
     "Johann Wolfgang von Goethe"),

    # Present Moment
    ("Yesterday is history, tomorrow is a mystery, today is a gift of God, which is why we call it the present.",
     "Bil Keane"),

    ("The best time to plant a tree was 20 years ago. The second best time is now.",
     "Chinese proverb"),

    ("Dream as if you'll live forever, live as if you'll die today.",
     "James Dean"),

    ("This is the beginning of a new day. You have been given this day to use as you will.",
     "Heartsill Wilson"),

    ("Today's accomplishments were yesterday's impossibilities.",
     "Robert H. Schuller"),

    ("Carpe diem. Seize the day, boys. Make your lives extraordinary.",
     "John Keating, 'Dead Poets Society' (1989)"),

    ("Not all those who wander are lost.",
     "J.R.R. Tolkien, 'The Lord of the Rings' (1954)"),

    # Hustle / Success
    ("Success usually comes to those who are too busy to be looking for it.",
     "Henry David Thoreau"),

    ("Opportunities don't happen. You create them.",
     "Chris Grosser"),

    ("I find that the harder I work, the more luck I seem to have.",
     "Thomas Jefferson"),

    ("The way to get started is to quit talking and begin doing.",
     "Walt Disney"),

    ("If you are not willing to risk the usual, you will have to settle for the ordinary.",
     "Jim Rohn"),

    ("Success is walking from failure to failure with no loss of enthusiasm.",
     "Winston Churchill"),

    ("Dream big. Start small. Act now.",
     "Robin Sharma"),

    ("Hustle until your haters ask if you're hiring.",
     "Steve Maraboli"),

    ("Energy and persistence conquer all things.",
     "Benjamin Franklin"),

    ("Great things never come from comfort zones.",
     "Unknown"),

    # Joy & Gratitude
    ("When you arise in the morning, think of what a precious privilege it is to be alive — to breathe, to think, to enjoy, to love.",
     "Marcus Aurelius, 'Meditations'"),

    ("Happiness is not something ready-made. It comes from your own actions.",
     "Dalai Lama XIV"),

    ("The more you praise and celebrate your life, the more there is in life to celebrate.",
     "Oprah Winfrey"),

    ("Joy does not simply happen to us. We have to choose joy and keep choosing it every day.",
     "Henri Nouwen"),

    ("Count your age by friends, not years. Count your life by smiles, not tears.",
     "John Lennon"),

    ("Gratitude turns what we have into enough.",
     "Unknown"),

    ("The secret of happiness is not in doing what one likes, but in liking what one does.",
     "James M. Barrie"),

    ("For every minute you are angry you lose sixty seconds of happiness.",
     "Ralph Waldo Emerson"),

    ("Laughter is timeless, imagination has no age, dreams are forever.",
     "Walt Disney"),
]


def pick_quote_for_today():
    """Pick a quote deterministically based on today's date."""
    today_str = date.today().isoformat()
    idx = int(hashlib.md5(today_str.encode()).hexdigest(), 16) % len(QUOTES)
    return QUOTES[idx]


def build_email_html(quote_text: str, source: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: Georgia, 'Times New Roman', serif;
      background: #f9f7f4;
      margin: 0;
      padding: 40px 20px;
    }}
    .card {{
      max-width: 600px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
      padding: 48px 40px;
      text-align: center;
    }}
    .emoji {{
      font-size: 48px;
      margin-bottom: 24px;
    }}
    .quote {{
      font-size: 22px;
      line-height: 1.65;
      color: #1a1a2e;
      font-style: italic;
      margin: 0 0 28px 0;
    }}
    .divider {{
      width: 48px;
      height: 3px;
      background: #f4845f;
      border-radius: 2px;
      margin: 0 auto 24px;
    }}
    .source {{
      font-size: 14px;
      color: #888;
      letter-spacing: 0.5px;
    }}
    .footer {{
      margin-top: 36px;
      font-size: 12px;
      color: #bbb;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="emoji">&#9728;&#65039;</div>
    <p class="quote">&#8220;{quote_text}&#8221;</p>
    <div class="divider"></div>
    <p class="source">— {source}</p>
    <div class="footer">Your daily morning quote &bull; Have a powerful day!</div>
  </div>
</body>
</html>
"""


def send_quote():
    if not APP_PASSWORD:
        print("ERROR: No Gmail app password found.", file=sys.stderr)
        print("Set env var GMAIL_APP_PASSWORD or write it to .gmail_app_password", file=sys.stderr)
        sys.exit(1)

    quote_text, source = pick_quote_for_today()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{SUBJECT_PREFIX}: \"{quote_text[:60]}{'...' if len(quote_text) > 60 else ''}\""
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    plain = f'"{quote_text}"\n\n— {source}\n\nHave a powerful day!'
    html = build_email_html(quote_text, source)

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())

    print(f"Sent quote: \"{quote_text[:80]}...\"")
    print(f"Source: {source}")


if __name__ == "__main__":
    send_quote()
