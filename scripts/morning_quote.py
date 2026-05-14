#!/usr/bin/env python3
"""Daily morning quote sender via KakaoTalk 나에게 보내기."""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

QUOTES = [
    # Movies
    ("Get busy living, or get busy dying.", "The Shawshank Redemption"),
    ("Do, or do not. There is no try.", "Yoda — The Empire Strikes Back"),
    ("Why do we fall? So we can learn to pick ourselves up.", "Alfred — Batman Begins"),
    ("Hope is a good thing, maybe the best of things, and no good thing ever dies.", "The Shawshank Redemption"),
    ("Carpe diem. Seize the day. Make your lives extraordinary.", "Dead Poets Society"),
    ("You is kind, you is smart, you is important.", "The Help"),
    ("We accept the love we think we deserve.", "The Perks of Being a Wallflower"),
    ("Every passing minute is another chance to turn it all around.", "Vanilla Sky"),
    ("It's not who I am underneath, but what I do that defines me.", "Batman Begins"),
    ("Ohana means family. Nobody gets left behind or forgotten.", "Lilo & Stitch"),
    ("It is not our abilities that show what we truly are. It is our choices.", "Dumbledore — Harry Potter"),
    ("Not all those who wander are lost.", "J.R.R. Tolkien — The Fellowship of the Ring"),
    ("Even the smallest person can change the course of the future.", "Galadriel — The Lord of the Rings"),
    ("After all this time? Always.", "Snape — Harry Potter and the Deathly Hallows"),
    ("Words are our most inexhaustible source of magic.", "Dumbledore — Harry Potter"),
    ("Just keep swimming.", "Dory — Finding Nemo"),
    ("To infinity and beyond!", "Buzz Lightyear — Toy Story"),
    ("The flower that blooms in adversity is the most rare and beautiful of all.", "Mulan"),

    # Speeches & Historical Figures
    ("Ask not what your country can do for you — ask what you can do for your country.", "John F. Kennedy"),
    ("The time is always right to do what is right.", "Martin Luther King Jr."),
    ("If you're going through hell, keep going.", "Winston Churchill"),
    ("We are the ones we've been waiting for.", "June Jordan"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("I have not failed. I've found 10,000 ways that won't work.", "Thomas Edison"),
    ("Spread love everywhere you go.", "Mother Teresa"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("Try to become a man of value rather than a man of success.", "Albert Einstein"),
    ("Imagination is more important than knowledge.", "Albert Einstein"),
    ("The best way to predict the future is to create it.", "Abraham Lincoln"),
    ("When you reach the end of your rope, tie a knot and hang on.", "Franklin D. Roosevelt"),
    ("No one can make you feel inferior without your consent.", "Eleanor Roosevelt"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Do one thing every day that scares you.", "Eleanor Roosevelt"),
    ("Be yourself; everyone else is already taken.", "Oscar Wilde"),
    ("That which does not kill us makes us stronger.", "Friedrich Nietzsche"),
    ("To live is the rarest thing in the world. Most people just exist.", "Oscar Wilde"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
    ("Stay hungry. Stay foolish.", "Steve Jobs — Stanford Commencement 2005"),
    ("The people who are crazy enough to think they can change the world are the ones who do.", "Steve Jobs"),
    ("Whether you think you can or think you can't, you're right.", "Henry Ford"),
    ("Don't count the days, make the days count.", "Muhammad Ali"),
    ("I am not a product of my circumstances. I am a product of my decisions.", "Stephen Covey"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Keep your face toward the sunshine and shadows will fall behind you.", "Walt Whitman"),
    ("Two roads diverged in a wood, and I took the one less traveled by.", "Robert Frost"),

    # Books
    ("We are all of us stars, and we deserve to twinkle.", "Marilyn Monroe"),
    ("Life is what happens when you're busy making other plans.", "John Lennon — Beautiful Boy"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It's the possibility of having a dream come true that makes life interesting.", "Paulo Coelho — The Alchemist"),
    ("And, when you want something, all the universe conspires to help you achieve it.", "Paulo Coelho — The Alchemist"),
    ("You are braver than you believe, stronger than you seem, and smarter than you think.", "A.A. Milne — Winnie-the-Pooh"),
    ("Sometimes the smallest things take up the most room in your heart.", "A.A. Milne — Winnie-the-Pooh"),
    ("You have power over your mind, not outside events. Realize this and you will find strength.", "Marcus Aurelius — Meditations"),
    ("The impediment to action advances action. What stands in the way becomes the way.", "Marcus Aurelius"),
    ("Very little is needed to make a happy life; it is all within yourself, in your way of thinking.", "Marcus Aurelius"),
    ("We suffer more in imagination than in reality.", "Seneca"),
    ("It is not that I'm so smart, it's just that I stay with problems longer.", "Albert Einstein"),
    ("Done is better than perfect.", "Sheryl Sandberg — Lean In"),
    ("Vulnerability is the birthplace of innovation, creativity, and change.", "Brené Brown — Daring Greatly"),
    ("Fall seven times, stand up eight.", "Japanese Proverb"),

    # Songs
    ("What doesn't kill you makes you stronger, stand a little taller.", "Kelly Clarkson — Stronger"),
    ("Don't stop believin'. Hold on to the feelin'.", "Journey — Don't Stop Believin'"),
    ("We are the champions, my friends. And we'll keep on fighting 'til the end.", "Queen — We Are the Champions"),
    ("I will survive. As long as I know how to love, I know I'll stay alive.", "Gloria Gaynor — I Will Survive"),
    ("Started from the bottom, now we're here.", "Drake — Started from the Bottom"),
    ("Roar. I am a champion and you're gonna hear me roar.", "Katy Perry — Roar"),
    ("Shake it off. The haters gonna hate, hate, hate, hate, hate.", "Taylor Swift — Shake It Off"),
    ("This is me. Look out, 'cause here I come.", "The Greatest Showman — This Is Me"),
    ("For good, I have been changed. Because I knew you.", "Wicked — For Good"),
    ("Reach for the stars. Climb every mountain higher.", "S Club 7 — Reach"),

    # Podcasts & Modern Voices
    ("The only impossible journey is the one you never begin.", "Tony Robbins"),
    ("Where focus goes, energy flows.", "Tony Robbins"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("You are enough, a thousand times enough.", "Atticus"),
    ("The cave you fear to enter holds the treasure you seek.", "Joseph Campbell"),
    ("Your only limit is your mind.", "Unknown"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Be the change you wish to see in the world.", "Mahatma Gandhi"),
    ("In the depth of winter, I finally learned there was in me an invincible summer.", "Albert Camus"),
    ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
    ("The best revenge is massive success.", "Frank Sinatra"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Stars can't shine without darkness.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
]


def get_access_token(client_id: str, refresh_token: str) -> str:
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }).encode()
    req = urllib.request.Request(
        "https://kauth.kakao.com/oauth/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]


def send_kakao_memo(access_token: str, message: str) -> dict:
    template = json.dumps({
        "object_type": "text",
        "text": message,
        "link": {"web_url": "", "mobile_web_url": ""},
    })
    data = urllib.parse.urlencode({"template_object": template}).encode()
    req = urllib.request.Request(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    client_id = os.environ["KAKAO_CLIENT_ID"]
    refresh_token = os.environ["KAKAO_REFRESH_TOKEN"]

    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst)
    day_of_year = now_kst.timetuple().tm_yday
    quote, source = QUOTES[day_of_year % len(QUOTES)]

    message = f'🌅 Morning fuel:\n\n"{quote}"\n— {source}\n\nGo be amazing! 🔥'
    print(f"Sending ({len(message)} chars):\n{message}\n")

    access_token = get_access_token(client_id, refresh_token)
    result = send_kakao_memo(access_token, message)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
