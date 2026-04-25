#!/usr/bin/env python3
"""
Daily inspirational quote mailer — runs via cron at 10am every day.
Credentials are read from ~/.daily_quote.env
"""

import smtplib
import ssl
import os
import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── credentials ──────────────────────────────────────────────────────────────
def load_env(path=Path.home() / ".daily_quote.env"):
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env()

GMAIL_USER = os.environ["GMAIL_USER"]          # your Gmail address
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]  # 16-char app password
TO_EMAIL = os.environ.get("TO_EMAIL", GMAIL_USER)

# ── quote library ─────────────────────────────────────────────────────────────
QUOTES = [
    # Movies
    ("You is kind, you is smart, you is important.",
     "Aibileen Clark — The Help (2011)"),
    ("Why so serious? … Why so serious?! Let's put a smile on that face.",
     "The Joker — The Dark Knight (2008)"),
    ("It ain't about how hard you hit. It's about how hard you can get hit and keep moving forward.",
     "Rocky Balboa — Rocky Balboa (2006)"),
    ("After all, tomorrow is another day!",
     "Scarlett O'Hara — Gone with the Wind (1939)"),
    ("Get busy living, or get busy dying.",
     "Andy Dufresne — The Shawshank Redemption (1994)"),
    ("To infinity and beyond!",
     "Buzz Lightyear — Toy Story (1995)"),
    ("Do, or do not. There is no try.",
     "Yoda — Star Wars: The Empire Strikes Back (1980)"),
    ("You can't handle the truth!",
     "Col. Jessup — A Few Good Men (1992)"),
    ("Every passing minute is another chance to turn it all around.",
     "Sofia — Vanilla Sky (2001)"),
    ("Just keep swimming.",
     "Dory — Finding Nemo (2003)"),
    ("Life is like a box of chocolates; you never know what you're gonna get.",
     "Forrest Gump — Forrest Gump (1994)"),
    ("The stuff that dreams are made of.",
     "Sam Spade — The Maltese Falcon (1941)"),
    ("We accept the love we think we deserve.",
     "Bill — The Perks of Being a Wallflower (2012)"),
    ("All those moments will be lost in time, like tears in rain.",
     "Roy Batty — Blade Runner (1982)"),
    ("Nobody puts Baby in a corner.",
     "Johnny Castle — Dirty Dancing (1987)"),
    ("You had me at hello.",
     "Dorothy Boyd — Jerry Maguire (1996)"),
    ("Carpe diem. Seize the day, boys. Make your lives extraordinary.",
     "John Keating — Dead Poets Society (1989)"),
    ("Our lives are defined by opportunities, even the ones we miss.",
     "Benjamin Button — The Curious Case of Benjamin Button (2008)"),
    ("With great power comes great responsibility.",
     "Uncle Ben — Spider-Man (2002)"),
    ("I'm the king of the world!",
     "Jack Dawson — Titanic (1997)"),
    ("Great men are not born great, they grow great.",
     "Mario Puzo — The Godfather (1972 film)"),

    # Sports / Athletes
    ("I've missed more than 9,000 shots in my career. I've lost almost 300 games. I've failed over and over. And that is why I succeed.",
     "Michael Jordan"),
    ("The most important thing is to try and inspire people so that they can be great in whatever they want to do.",
     "Kobe Bryant"),
    ("You miss 100% of the shots you don't take.",
     "Wayne Gretzky"),
    ("Hard work beats talent when talent doesn't work hard.",
     "Tim Notke (popularized by Kevin Durant)"),
    ("Don't be afraid of failure. This is the way to succeed.",
     "LeBron James"),
    ("The more difficult the victory, the greater the happiness in winning.",
     "Pelé"),
    ("Champions keep playing until they get it right.",
     "Billie Jean King"),
    ("You have to expect things of yourself before you can do them.",
     "Michael Jordan"),
    ("I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'",
     "Muhammad Ali"),
    ("Float like a butterfly, sting like a bee.",
     "Muhammad Ali"),
    ("It always seems impossible until it's done.",
     "Nelson Mandela (also attributed to sports)"),
    ("The only way to prove you are a good sport is to lose.",
     "Ernie Banks"),
    ("You are never really playing an opponent. You are playing yourself.",
     "Arthur Ashe"),
    ("Make each day your masterpiece.",
     "John Wooden"),
    ("Winning is not a sometime thing; it's an all-time thing.",
     "Vince Lombardi"),
    ("The difference between the impossible and the possible lies in a person's determination.",
     "Tommy Lasorda"),
    ("Once you learn to quit, it becomes a habit.",
     "Vince Lombardi"),
    ("Do you know what my favorite part of the game is? The opportunity to play.",
     "Mike Singletary"),
    ("Talent wins games, but teamwork and intelligence wins championships.",
     "Michael Jordan"),
    ("Push yourself again and again. Don't give an inch until the final buzzer sounds.",
     "Larry Bird"),

    # Speeches / Historical Figures
    ("The time is always right to do what is right.",
     "Martin Luther King Jr."),
    ("Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
     "Martin Luther King Jr."),
    ("The only thing we have to fear is fear itself.",
     "Franklin D. Roosevelt — First Inaugural Address, 1933"),
    ("Ask not what your country can do for you—ask what you can do for your country.",
     "John F. Kennedy — Inaugural Address, 1961"),
    ("We shall fight on the beaches… we shall never surrender.",
     "Winston Churchill — House of Commons, June 1940"),
    ("I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.",
     "Martin Luther King Jr. — March on Washington, 1963"),
    ("Well-behaved women seldom make history.",
     "Laurel Thatcher Ulrich"),
    ("In the middle of every difficulty lies opportunity.",
     "Albert Einstein"),
    ("Imagination is more important than knowledge.",
     "Albert Einstein"),
    ("Logic will get you from A to B. Imagination will take you everywhere.",
     "Albert Einstein"),
    ("The secret of getting ahead is getting started.",
     "Mark Twain"),
    ("The man who has no imagination has no wings.",
     "Muhammad Ali"),
    ("I am not a product of my circumstances. I am a product of my decisions.",
     "Stephen Covey"),
    ("Either you run the day or the day runs you.",
     "Jim Rohn"),
    ("We must accept finite disappointment, but never lose infinite hope.",
     "Martin Luther King Jr."),
    ("In the end, it's not the years in your life that count. It's the life in your years.",
     "Abraham Lincoln"),
    ("Two roads diverged in a wood, and I—I took the one less traveled by.",
     "Robert Frost — The Road Not Taken"),
    ("Do not go where the path may lead; go instead where there is no path and leave a trail.",
     "Ralph Waldo Emerson"),
    ("What you do speaks so loudly that I cannot hear what you say.",
     "Ralph Waldo Emerson"),
    ("The only person you are destined to become is the person you decide to be.",
     "Ralph Waldo Emerson"),

    # Books / Literature
    ("It does not do to dwell on dreams and forget to live.",
     "Albus Dumbledore — Harry Potter and the Philosopher's Stone"),
    ("It is our choices, Harry, that show what we truly are, far more than our abilities.",
     "Albus Dumbledore — Harry Potter and the Chamber of Secrets"),
    ("Happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
     "Albus Dumbledore — Harry Potter and the Prisoner of Azkaban (film)"),
    ("Not all those who wander are lost.",
     "J.R.R. Tolkien — The Fellowship of the Ring"),
    ("Even the smallest person can change the course of the future.",
     "Galadriel — The Lord of the Rings"),
    ("There is some good in this world, and it's worth fighting for.",
     "J.R.R. Tolkien — The Two Towers"),
    ("It's the possibility of having a dream come true that makes life interesting.",
     "Paulo Coelho — The Alchemist"),
    ("When you want something, all the universe conspires in helping you to achieve it.",
     "Paulo Coelho — The Alchemist"),
    ("Life is what happens to us while we are making other plans.",
     "Allen Saunders (popularized by John Lennon)"),
    ("The journey of a thousand miles begins with one step.",
     "Lao Tzu"),
    ("Wherever you go, go with all your heart.",
     "Confucius"),
    ("In three words I can sum up everything I've learned about life: it goes on.",
     "Robert Frost"),
    ("You only live once, but if you do it right, once is enough.",
     "Mae West"),
    ("Be yourself; everyone else is already taken.",
     "Oscar Wilde"),
    ("Always be a first-rate version of yourself, not a second-rate version of someone else.",
     "Judy Garland"),
    ("To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
     "Ralph Waldo Emerson"),
    ("You can never cross the ocean unless you have the courage to lose sight of the shore.",
     "André Gide (often misattributed to Columbus)"),
    ("A reader lives a thousand lives before he dies. The man who never reads lives only one.",
     "George R.R. Martin — A Dance with Dragons"),

    # Tech / Business
    ("Your time is limited, so don't waste it living someone else's life.",
     "Steve Jobs — Stanford Commencement, 2005"),
    ("Stay hungry, stay foolish.",
     "Stewart Brand — The Whole Earth Catalog (cited by Steve Jobs)"),
    ("Innovation distinguishes between a leader and a follower.",
     "Steve Jobs"),
    ("The best way to predict the future is to create it.",
     "Peter Drucker"),
    ("Whether you think you can, or you think you can't—you're right.",
     "Henry Ford"),
    ("The greatest glory in living lies not in never falling, but in rising every time we fall.",
     "Nelson Mandela"),
    ("I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
     "Jimmy Dean"),
    ("It is not the strongest of the species that survive, nor the most intelligent, but the one most responsive to change.",
     "Charles Darwin (paraphrase)"),
    ("Success is not final; failure is not fatal: it is the courage to continue that counts.",
     "Winston Churchill"),
    ("I find that the harder I work, the more luck I seem to have.",
     "Thomas Jefferson"),
    ("The way to get started is to quit talking and begin doing.",
     "Walt Disney"),
    ("Eighty percent of success is showing up.",
     "Woody Allen"),
    ("I never dreamed about success. I worked for it.",
     "Estée Lauder"),
    ("The road to success and the road to failure are almost exactly the same.",
     "Colin R. Davis"),
    ("Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do.",
     "H. Jackson Brown Jr. (popularized by Mark Twain)"),
    ("Move fast and break things. Unless you are breaking stuff, you are not moving fast enough.",
     "Mark Zuckerberg"),
    ("If you're going through hell, keep going.",
     "Winston Churchill"),

    # Music / Songs
    ("What doesn't kill you makes you stronger.",
     "Kelly Clarkson — Stronger (2011)"),
    ("Roar. I am a champion, and you're gonna hear me roar.",
     "Katy Perry — Roar (2013)"),
    ("I will survive.",
     "Gloria Gaynor — I Will Survive (1978)"),
    ("Started from the bottom, now we're here.",
     "Drake — Started from the Bottom (2013)"),
    ("Don't stop believin'.",
     "Journey — Don't Stop Believin' (1981)"),
    ("We are the champions, my friends, and we'll keep on fighting till the end.",
     "Queen — We Are the Champions (1977)"),
    ("Rise up. Rise up.",
     "Andra Day — Rise Up (2015)"),
    ("With a little help from my friends.",
     "The Beatles — With a Little Help from My Friends (1967)"),
    ("Run the world.",
     "Beyoncé — Run the World (Girls) (2011)"),
    ("Shake it off.",
     "Taylor Swift — Shake It Off (2014)"),
    ("I believe I can fly.",
     "R. Kelly — I Believe I Can Fly (1996)"),
    ("Here I am, this is me. There's nowhere else on Earth I'd rather be.",
     "Phil Collins — Two Worlds (Tarzan OST, 1999)"),
    ("A little less conversation, a little more action.",
     "Elvis Presley — A Little Less Conversation (1968)"),

    # Philosophy / Wisdom
    ("He who has a why to live can bear almost any how.",
     "Friedrich Nietzsche"),
    ("The unexamined life is not worth living.",
     "Socrates"),
    ("Man is not the creature of circumstances; circumstances are the creatures of men.",
     "Benjamin Disraeli"),
    ("Knowing yourself is the beginning of all wisdom.",
     "Aristotle"),
    ("We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
     "Aristotle (via Will Durant)"),
    ("No man ever steps in the same river twice, for it's not the same river and he's not the same man.",
     "Heraclitus"),
    ("The obstacle is the path.",
     "Zen proverb"),
    ("Fall seven times, stand up eight.",
     "Japanese proverb"),
    ("You are the average of the five people you spend the most time with.",
     "Jim Rohn"),
    ("The mind is everything. What you think, you become.",
     "Buddha"),
    ("Peace comes from within. Do not seek it without.",
     "Buddha"),
    ("All that we are is the result of what we have thought.",
     "Buddha"),
    ("Simplicity is the ultimate sophistication.",
     "Leonardo da Vinci"),
    ("Learning never exhausts the mind.",
     "Leonardo da Vinci"),
    ("An unexamined life is not worth living. A life unlived is not worth examining.",
     "adapted from Socrates"),
    ("Those who dare to fail miserably can achieve greatly.",
     "Robert F. Kennedy"),
    ("Only those who will risk going too far can possibly find out how far one can go.",
     "T.S. Eliot"),
    ("The purpose of our lives is to be happy.",
     "Dalai Lama"),
    ("Not enough sleep is a recipe for mediocrity. Guard your rest.",
     "Matthew Walker — Why We Sleep"),
    ("The cave you fear to enter holds the treasure you seek.",
     "Joseph Campbell"),
    ("Life shrinks or expands in proportion to one's courage.",
     "Anaïs Nin"),
]

# ── quote selection ────────────────────────────────────────────────────────────
def pick_quote():
    today = datetime.date.today()
    # deterministic per calendar day, cycles through the full list
    idx = (today.toordinal()) % len(QUOTES)
    return QUOTES[idx]

# ── email ─────────────────────────────────────────────────────────────────────
HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: Georgia, 'Times New Roman', serif;
    background: #f9f6f0;
    margin: 0;
    padding: 0;
  }}
  .wrapper {{
    max-width: 560px;
    margin: 40px auto;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  }}
  .banner {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 36px 40px 28px;
    text-align: center;
  }}
  .banner .label {{
    color: #e2b96f;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .banner .day {{
    color: #ffffff;
    font-size: 14px;
    opacity: 0.7;
    font-style: italic;
  }}
  .body {{
    padding: 40px 44px 36px;
  }}
  blockquote {{
    margin: 0 0 24px;
    padding: 0 0 0 20px;
    border-left: 4px solid #e2b96f;
    font-size: 22px;
    line-height: 1.55;
    color: #1a1a2e;
    font-style: italic;
  }}
  .attribution {{
    color: #888;
    font-size: 13px;
    font-style: normal;
    margin-top: 18px;
    padding-top: 18px;
    border-top: 1px solid #eee;
  }}
  .attribution strong {{
    color: #444;
  }}
  .footer {{
    text-align: center;
    padding: 16px;
    font-size: 11px;
    color: #bbb;
    background: #fafafa;
  }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="banner">
    <div class="label">Your Morning Quote</div>
    <div class="day">{date_str}</div>
  </div>
  <div class="body">
    <blockquote>"{quote}"</blockquote>
    <div class="attribution">— <strong>{attribution}</strong></div>
  </div>
  <div class="footer">Have an incredible day. You've got this.</div>
</div>
</body>
</html>
"""

def send_quote():
    quote, attribution = pick_quote()
    today = datetime.date.today()
    date_str = today.strftime("%A, %B %-d, %Y")

    subject = f"Your Morning Quote — {date_str}"
    html_body = HTML_TEMPLATE.format(
        date_str=date_str,
        quote=quote.replace('"', "&ldquo;").replace('"', "&rdquo;"),
        attribution=attribution,
    )
    plain_body = f'"{quote}"\n\n— {attribution}\n\nHave an incredible day.'

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())

    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] Sent quote to {TO_EMAIL}: \"{quote[:60]}...\"" )

if __name__ == "__main__":
    send_quote()
