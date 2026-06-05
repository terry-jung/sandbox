#!/usr/bin/env python3
import smtplib
import os
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

QUOTES = [
    {
        "quote": "You have power over your mind — not outside events. Realize this, and you will find strength.",
        "source": "Marcus Aurelius, Meditations",
    },
    {
        "quote": "It does not matter how slowly you go as long as you do not stop.",
        "source": "Confucius",
    },
    {
        "quote": "The only way to do great work is to love what you do.",
        "source": "Steve Jobs, Stanford Commencement Speech (2005)",
    },
    {
        "quote": "You miss 100% of the shots you don't take.",
        "source": "Wayne Gretzky",
    },
    {
        "quote": "Whether you think you can or you think you can't — you're right.",
        "source": "Henry Ford",
    },
    {
        "quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
        "source": "Aristotle (via Will Durant, The Story of Philosophy)",
    },
    {
        "quote": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "source": "Nelson Mandela",
    },
    {
        "quote": "I am not a product of my circumstances. I am a product of my decisions.",
        "source": "Stephen Covey, The 7 Habits of Highly Effective People",
    },
    {
        "quote": "In the middle of every difficulty lies opportunity.",
        "source": "Albert Einstein",
    },
    {
        "quote": "The secret of getting ahead is getting started.",
        "source": "Mark Twain",
    },
    {
        "quote": "Don't watch the clock; do what it does. Keep going.",
        "source": "Sam Levenson",
    },
    {
        "quote": "Believe you can and you're halfway there.",
        "source": "Theodore Roosevelt",
    },
    {
        "quote": "Life is not measured by the number of breaths we take, but by the moments that take our breath away.",
        "source": "Maya Angelou",
    },
    {
        "quote": "You only live once, but if you do it right, once is enough.",
        "source": "Mae West",
    },
    {
        "quote": "Get busy living, or get busy dying.",
        "source": "The Shawshank Redemption (1994)",
    },
    {
        "quote": "Every moment is a fresh beginning.",
        "source": "T.S. Eliot",
    },
    {
        "quote": "Keep your face always toward the sunshine, and shadows will fall behind you.",
        "source": "Walt Whitman",
    },
    {
        "quote": "The future belongs to those who believe in the beauty of their dreams.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "It always seems impossible until it's done.",
        "source": "Nelson Mandela",
    },
    {
        "quote": "Your time is limited, so don't waste it living someone else's life.",
        "source": "Steve Jobs, Stanford Commencement Speech (2005)",
    },
    {
        "quote": "Stars can't shine without darkness.",
        "source": "D.H. Sidebottom, Beautifully Broken",
    },
    {
        "quote": "The only limit to our realization of tomorrow will be our doubts of today.",
        "source": "Franklin D. Roosevelt",
    },
    {
        "quote": "Everything you've ever wanted is on the other side of fear.",
        "source": "George Addair",
    },
    {
        "quote": "You are never too old to set another goal or to dream a new dream.",
        "source": "C.S. Lewis",
    },
    {
        "quote": "Act as if what you do makes a difference. It does.",
        "source": "William James",
    },
    {
        "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "source": "Winston Churchill",
    },
    {
        "quote": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
        "source": "Ralph Waldo Emerson",
    },
    {
        "quote": "Two roads diverged in a wood, and I — I took the one less traveled by, and that has made all the difference.",
        "source": "Robert Frost, The Road Not Taken",
    },
    {
        "quote": "Life isn't about finding yourself. Life is about creating yourself.",
        "source": "George Bernard Shaw",
    },
    {
        "quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
        "source": "Ralph Waldo Emerson",
    },
    {
        "quote": "The man who moves a mountain begins by carrying away small stones.",
        "source": "Confucius",
    },
    {
        "quote": "I can't change the direction of the wind, but I can adjust my sails to always reach my destination.",
        "source": "Jimmy Dean",
    },
    {
        "quote": "You've got to get up every morning with determination if you're going to go to bed with satisfaction.",
        "source": "George Lorimer",
    },
    {
        "quote": "Do what you can, with what you have, where you are.",
        "source": "Theodore Roosevelt",
    },
    {
        "quote": "Fall seven times, stand up eight.",
        "source": "Japanese proverb",
    },
    {
        "quote": "It is during our darkest moments that we must focus to see the light.",
        "source": "Aristotle",
    },
    {
        "quote": "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
        "source": "Mother Teresa",
    },
    {
        "quote": "When you reach the end of your rope, tie a knot in it and hang on.",
        "source": "Franklin D. Roosevelt",
    },
    {
        "quote": "Always remember that you are absolutely unique. Just like everyone else.",
        "source": "Margaret Mead",
    },
    {
        "quote": "Do not go where the path may lead, go instead where there is no path and leave a trail.",
        "source": "Ralph Waldo Emerson",
    },
    {
        "quote": "You will face many defeats in life, but never let yourself be defeated.",
        "source": "Maya Angelou",
    },
    {
        "quote": "The most common way people give up their power is by thinking they don't have any.",
        "source": "Alice Walker",
    },
    {
        "quote": "You must be the change you wish to see in the world.",
        "source": "Mahatma Gandhi",
    },
    {
        "quote": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
        "source": "Martin Luther King Jr., Strength to Love",
    },
    {
        "quote": "Shoot for the moon. Even if you miss, you'll land among the stars.",
        "source": "Norman Vincent Peale",
    },
    {
        "quote": "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.",
        "source": "Maya Angelou",
    },
    {
        "quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "source": "Chinese proverb",
    },
    {
        "quote": "An unexamined life is not worth living.",
        "source": "Socrates",
    },
    {
        "quote": "Spread your wings and let the fairy in you fly!",
        "source": "Rumi, The Essential Rumi",
    },
    {
        "quote": "Out of difficulties grow miracles.",
        "source": "Jean de La Bruyère",
    },
    {
        "quote": "First, say to yourself what you would be; and then do what you have to do.",
        "source": "Epictetus",
    },
    {
        "quote": "Hardships often prepare ordinary people for an extraordinary destiny.",
        "source": "C.S. Lewis",
    },
    {
        "quote": "The difference between ordinary and extraordinary is that little extra.",
        "source": "Jimmy Johnson",
    },
    {
        "quote": "Nothing is impossible. The word itself says 'I'm possible!'",
        "source": "Audrey Hepburn",
    },
    {
        "quote": "It's not whether you get knocked down, it's whether you get up.",
        "source": "Vince Lombardi",
    },
    {
        "quote": "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough.",
        "source": "Oprah Winfrey",
    },
    {
        "quote": "Remember no one can make you feel inferior without your consent.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "You are the sum total of everything you've ever seen, heard, eaten, smelled, been told, forgot — it's all there.",
        "source": "Maya Angelou",
    },
    {
        "quote": "Life is what happens to us while we are making other plans.",
        "source": "Allen Saunders (popularized by John Lennon)",
    },
    {
        "quote": "I am not afraid of storms, for I am learning how to sail my ship.",
        "source": "Louisa May Alcott, Little Women",
    },
    {
        "quote": "Start where you are. Use what you have. Do what you can.",
        "source": "Arthur Ashe",
    },
    {
        "quote": "The only person you are destined to become is the person you decide to be.",
        "source": "Ralph Waldo Emerson",
    },
    {
        "quote": "Go confidently in the direction of your dreams. Live the life you have imagined.",
        "source": "Henry David Thoreau",
    },
    {
        "quote": "When I stand before God at the end of my life, I would hope that I would not have a single bit of talent left, and could say, 'I used everything you gave me.'",
        "source": "Erma Bombeck",
    },
    {
        "quote": "Few things can help an individual more than to place responsibility on him, and to let him know that you trust him.",
        "source": "Booker T. Washington",
    },
    {
        "quote": "Perfection is not attainable, but if we chase perfection we can catch excellence.",
        "source": "Vince Lombardi",
    },
    {
        "quote": "Do what you feel in your heart to be right — for you'll be criticized anyway.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "You can't use up creativity. The more you use, the more you have.",
        "source": "Maya Angelou",
    },
    {
        "quote": "I have not failed. I've just found 10,000 ways that won't work.",
        "source": "Thomas Edison",
    },
    {
        "quote": "A person who never made a mistake never tried anything new.",
        "source": "Albert Einstein",
    },
    {
        "quote": "Great minds discuss ideas; average minds discuss events; small minds discuss people.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "I have learned over the years that when one's mind is made up, this diminishes fear.",
        "source": "Rosa Parks",
    },
    {
        "quote": "I alone cannot change the world, but I can cast a stone across the water to create many ripples.",
        "source": "Mother Teresa",
    },
    {
        "quote": "Nothing is impossible, the word itself says 'I'm possible'!",
        "source": "Audrey Hepburn",
    },
    {
        "quote": "The question isn't who is going to let me; it's who is going to stop me.",
        "source": "Ayn Rand, The Fountainhead",
    },
    {
        "quote": "Once you choose hope, anything's possible.",
        "source": "Christopher Reeve",
    },
    {
        "quote": "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.",
        "source": "Dr. Seuss, Oh, the Places You'll Go!",
    },
    {
        "quote": "If life were predictable it would cease to be life, and be without flavor.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "In order to write about life first you must live it.",
        "source": "Ernest Hemingway",
    },
    {
        "quote": "The big lesson in life, baby, is never be scared of anyone or anything.",
        "source": "Frank Sinatra",
    },
    {
        "quote": "Sing like no one is listening, love like you've never been hurt, dance like nobody's watching, and live like it's heaven on earth.",
        "source": "Mark Twain",
    },
    {
        "quote": "When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us.",
        "source": "Helen Keller",
    },
    {
        "quote": "Life is not measured by the number of breaths you take but by the moments that take your breath away.",
        "source": "George Carlin",
    },
    {
        "quote": "If you want to live a happy life, tie it to a goal, not to people or things.",
        "source": "Albert Einstein",
    },
    {
        "quote": "Never let the fear of striking out keep you from playing the game.",
        "source": "Babe Ruth",
    },
    {
        "quote": "Money and success don't change people; they merely amplify what is already there.",
        "source": "Will Smith",
    },
    {
        "quote": "Your talent is God's gift to you. What you do with it is your gift back to God.",
        "source": "Leo Buscaglia",
    },
    {
        "quote": "You can't go back and change the beginning, but you can start where you are and change the ending.",
        "source": "C.S. Lewis",
    },
    {
        "quote": "I would rather die of passion than of boredom.",
        "source": "Vincent van Gogh",
    },
    {
        "quote": "A truly rich man is one whose children run into his arms when his hands are empty.",
        "source": "Unknown",
    },
    {
        "quote": "If you do what you've always done, you'll get what you've always gotten.",
        "source": "Tony Robbins",
    },
    {
        "quote": "Dreaming, after all, is a form of planning.",
        "source": "Gloria Steinem",
    },
    {
        "quote": "It's not what you look at that matters, it's what you see.",
        "source": "Henry David Thoreau",
    },
    {
        "quote": "The only journey is the one within.",
        "source": "Rainer Maria Rilke, Letters to a Young Poet",
    },
    {
        "quote": "You've gotta dance like there's nobody watching, love like you'll never be hurt, sing like there's nobody listening, and live like it's heaven on earth.",
        "source": "William W. Purkey",
    },
    {
        "quote": "The purpose of our lives is to be happy.",
        "source": "Dalai Lama",
    },
    {
        "quote": "Get busy living or get busy dying.",
        "source": "Stephen King, Different Seasons (also The Shawshank Redemption)",
    },
    {
        "quote": "You only live once, but if you do it right, once is enough.",
        "source": "Mae West",
    },
    {
        "quote": "Many of life's failures are people who did not realize how close they were to success when they gave up.",
        "source": "Thomas Edison",
    },
    {
        "quote": "If you want to achieve greatness, stop asking for permission.",
        "source": "Anonymous",
    },
    {
        "quote": "Things work out best for those who make the best of how things work out.",
        "source": "John Wooden",
    },
    {
        "quote": "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do.",
        "source": "Mark Twain",
    },
    {
        "quote": "We generate fears while we sit. We overcome them by action.",
        "source": "Dr. Henry Link",
    },
    {
        "quote": "Whether you think you can or you think you can't, you're right.",
        "source": "Henry Ford",
    },
    {
        "quote": "The man who has confidence in himself gains the confidence of others.",
        "source": "Hasidic proverb",
    },
    {
        "quote": "The only way to achieve the impossible is to believe it is possible.",
        "source": "Charles Kingsleigh, Alice in Wonderland (2010)",
    },
    {
        "quote": "Even if I knew that tomorrow the world would go to pieces, I would still plant my apple tree.",
        "source": "Martin Luther King Jr.",
    },
    {
        "quote": "Believe in yourself! Have faith in your abilities! Without a humble but reasonable confidence in your own powers you cannot be successful or happy.",
        "source": "Norman Vincent Peale, The Power of Positive Thinking",
    },
    {
        "quote": "Try to be a rainbow in someone's cloud.",
        "source": "Maya Angelou",
    },
    {
        "quote": "I am grateful for all of my problems. After each one was resolved, I became stronger and more able to meet those that were still to come.",
        "source": "J.C. Penney",
    },
    {
        "quote": "I have found that if you love life, life will love you back.",
        "source": "Arthur Rubinstein",
    },
    {
        "quote": "Don't let yesterday take up too much of today.",
        "source": "Will Rogers",
    },
    {
        "quote": "You learn more from failure than from success. Don't let it stop you. Failure builds character.",
        "source": "Unknown",
    },
    {
        "quote": "It's not the years in your life that count. It's the life in your years.",
        "source": "Abraham Lincoln",
    },
    {
        "quote": "Change your thoughts and you change your world.",
        "source": "Norman Vincent Peale",
    },
    {
        "quote": "Either write something worth reading or do something worth writing.",
        "source": "Benjamin Franklin",
    },
    {
        "quote": "Nothing will work unless you do.",
        "source": "Maya Angelou",
    },
    {
        "quote": "I wake up every morning and think to myself, 'How far can I push this company in the next 24 hours?'",
        "source": "Leah Busque",
    },
    {
        "quote": "If you genuinely want something, don't wait for it — teach yourself to be impatient.",
        "source": "Gurbaksh Chahal",
    },
    {
        "quote": "If you can dream it, you can do it.",
        "source": "Walt Disney",
    },
    {
        "quote": "Dream big and dare to fail.",
        "source": "Norman Vaughan",
    },
    {
        "quote": "All our dreams can come true if we have the courage to pursue them.",
        "source": "Walt Disney",
    },
    {
        "quote": "The secret of success is to do the common thing uncommonly well.",
        "source": "John D. Rockefeller Jr.",
    },
    {
        "quote": "I find that the harder I work, the more luck I seem to have.",
        "source": "Thomas Jefferson",
    },
    {
        "quote": "The starting point of all achievement is desire.",
        "source": "Napoleon Hill, Think and Grow Rich",
    },
    {
        "quote": "Success is the sum of small efforts, repeated day in and day out.",
        "source": "Robert Collier",
    },
    {
        "quote": "If you can't outplay them, outwork them.",
        "source": "Ben Hogan",
    },
    {
        "quote": "Big shots are only little shots who keep shooting.",
        "source": "Christopher Morley",
    },
    {
        "quote": "You can't build a reputation on what you are going to do.",
        "source": "Henry Ford",
    },
    {
        "quote": "Some people want it to happen, some wish it would happen, others make it happen.",
        "source": "Michael Jordan",
    },
    {
        "quote": "The harder the conflict, the more glorious the triumph.",
        "source": "Thomas Paine",
    },
    {
        "quote": "How wonderful it is that nobody need wait a single moment before starting to improve the world.",
        "source": "Anne Frank, The Diary of a Young Girl",
    },
    {
        "quote": "When you know better you do better.",
        "source": "Maya Angelou",
    },
    {
        "quote": "Optimism is the faith that leads to achievement. Nothing can be done without hope and confidence.",
        "source": "Helen Keller",
    },
    {
        "quote": "It is our choices, far more than our abilities, that show what we truly are.",
        "source": "J.K. Rowling, Harry Potter and the Chamber of Secrets",
    },
    {
        "quote": "Do not let what you cannot do interfere with what you can do.",
        "source": "John Wooden",
    },
    {
        "quote": "Today is the only day. Yesterday is gone.",
        "source": "John Wooden",
    },
    {
        "quote": "We can't help everyone, but everyone can help someone.",
        "source": "Ronald Reagan",
    },
    {
        "quote": "One day the people that didn't believe in you will tell everyone how they met you.",
        "source": "Johnny Depp",
    },
    {
        "quote": "A winner is a dreamer who never gives up.",
        "source": "Nelson Mandela",
    },
    {
        "quote": "If you don't build your dream, someone else will hire you to help them build theirs.",
        "source": "Dhirubhai Ambani",
    },
    {
        "quote": "You were born to win, but to be a winner, you must plan to win, prepare to win, and expect to win.",
        "source": "Zig Ziglar",
    },
    {
        "quote": "I attribute my success to this: I never gave or took any excuse.",
        "source": "Florence Nightingale",
    },
    {
        "quote": "The past cannot be changed. The future is yet in your power.",
        "source": "Unknown",
    },
    {
        "quote": "I can't imagine a person becoming a success who doesn't give this game of life everything he's got.",
        "source": "Walter Cronkite",
    },
    {
        "quote": "We become what we think about most of the time, and that's the strangest secret.",
        "source": "Earl Nightingale",
    },
    {
        "quote": "Failure is the condiment that gives success its flavor.",
        "source": "Truman Capote",
    },
    {
        "quote": "Vision without execution is just hallucination.",
        "source": "Henry Ford",
    },
    {
        "quote": "Limitations live only in our minds. But if we use our imaginations, our possibilities become limitless.",
        "source": "Jamie Paolinetti",
    },
    {
        "quote": "Expect problems and eat them for breakfast.",
        "source": "Alfred A. Montapert",
    },
    {
        "quote": "It's not about perfect. It's about effort. And when you bring that effort every single day, that's where transformation happens.",
        "source": "Jillian Michaels",
    },
    {
        "quote": "Do what you love and the money will follow.",
        "source": "Marsha Sinetar",
    },
    {
        "quote": "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.",
        "source": "Steve Jobs",
    },
    {
        "quote": "You have to be burning with an idea, or a problem, or a wrong that you want to right. If you're not passionate enough from the start, you'll never stick it out.",
        "source": "Steve Jobs",
    },
    {
        "quote": "I would rather have a mind opened by wonder than one closed by belief.",
        "source": "Gerry Spence",
    },
    {
        "quote": "Nolite te bastardes carborundorum. Don't let the bastards grind you down.",
        "source": "Margaret Atwood, The Handmaid's Tale",
    },
    {
        "quote": "We accept the love we think we deserve.",
        "source": "Stephen Chbosky, The Perks of Being a Wallflower",
    },
    {
        "quote": "Not all those who wander are lost.",
        "source": "J.R.R. Tolkien, The Lord of the Rings",
    },
    {
        "quote": "It does not do to dwell on dreams and forget to live.",
        "source": "J.K. Rowling, Harry Potter and the Sorcerer's Stone",
    },
    {
        "quote": "We are all faced with a series of great opportunities brilliantly disguised as impossible situations.",
        "source": "Chuck Swindoll",
    },
    {
        "quote": "Everything you want is on the other side of hard.",
        "source": "Eric Thomas (ET the Hip Hop Preacher), motivational speech",
    },
    {
        "quote": "Pain is temporary. It may last a minute, or an hour, or a day, or a year, but eventually it will subside and something else will take its place. If I quit, however, it lasts forever.",
        "source": "Lance Armstrong, It's Not About the Bike",
    },
    {
        "quote": "Champions keep playing until they get it right.",
        "source": "Billie Jean King",
    },
    {
        "quote": "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
        "source": "Roy T. Bennett, The Light in the Heart",
    },
    {
        "quote": "Without hard work, nothing grows but weeds.",
        "source": "Gordon B. Hinckley",
    },
    {
        "quote": "You are enough, you have enough, you do enough.",
        "source": "Brené Brown, Daring Greatly",
    },
    {
        "quote": "The most beautiful people we have known are those who have known defeat, known suffering, known struggle, known loss, and have found their way out of the depths.",
        "source": "Elisabeth Kübler-Ross",
    },
    {
        "quote": "Do one thing every day that scares you.",
        "source": "Eleanor Roosevelt",
    },
    {
        "quote": "Well-behaved women seldom make history.",
        "source": "Laurel Thatcher Ulrich",
    },
    {
        "quote": "The secret of life is to fall seven times and to get up eight times.",
        "source": "Paulo Coelho, The Alchemist",
    },
    {
        "quote": "And, when you want something, all the universe conspires in helping you to achieve it.",
        "source": "Paulo Coelho, The Alchemist",
    },
    {
        "quote": "One must always be careful of bookshelves and what is on them, for someone has read and loved and been changed by each of those books.",
        "source": "Cassandra Clare, Clockwork Angel",
    },
    {
        "quote": "Happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
        "source": "J.K. Rowling / Albus Dumbledore, Harry Potter and the Prisoner of Azkaban",
    },
    {
        "quote": "Just keep swimming.",
        "source": "Dory, Finding Nemo (2003)",
    },
    {
        "quote": "To infinity and beyond!",
        "source": "Buzz Lightyear, Toy Story (1995)",
    },
    {
        "quote": "Oh yes, the past can hurt. But the way I see it, you can either run from it or learn from it.",
        "source": "Rafiki, The Lion King (1994)",
    },
    {
        "quote": "The flower that blooms in adversity is the most rare and beautiful of all.",
        "source": "The Emperor, Mulan (1998)",
    },
    {
        "quote": "All we have to decide is what to do with the time that is given us.",
        "source": "Gandalf / J.R.R. Tolkien, The Fellowship of the Ring",
    },
    {
        "quote": "You is kind, you is smart, you is important.",
        "source": "Aibileen Clark, The Help (2011)",
    },
    {
        "quote": "Every day is a new beginning. Take a deep breath, smile, and start again.",
        "source": "Susan Gale",
    },
    {
        "quote": "The best way out is always through.",
        "source": "Robert Frost",
    },
    {
        "quote": "Throw me to the wolves and I will return leading the pack.",
        "source": "Unknown",
    },
    {
        "quote": "The comeback is always stronger than the setback.",
        "source": "Unknown",
    },
    {
        "quote": "Be fearless in the pursuit of what sets your soul on fire.",
        "source": "Jennifer Lee",
    },
    {
        "quote": "Don't tell me the sky's the limit when there are footprints on the moon.",
        "source": "Paul Brandt",
    },
    {
        "quote": "Work hard in silence. Let your success be the noise.",
        "source": "Frank Ocean",
    },
    {
        "quote": "However difficult life may seem, there is always something you can do and succeed at.",
        "source": "Stephen Hawking",
    },
    {
        "quote": "The most courageous act is still to think for yourself. Aloud.",
        "source": "Coco Chanel",
    },
    {
        "quote": "I never dreamed about success. I worked for it.",
        "source": "Estée Lauder",
    },
    {
        "quote": "We do not need magic to transform our world. We carry all of the power we need inside ourselves already.",
        "source": "J.K. Rowling, Harvard Commencement Speech (2008)",
    },
    {
        "quote": "You are braver than you believe, stronger than you seem, smarter than you think.",
        "source": "A.A. Milne, Winnie-the-Pooh",
    },
    {
        "quote": "It takes courage to grow up and become who you really are.",
        "source": "E.E. Cummings",
    },
    {
        "quote": "Your life does not get better by chance. It gets better by change.",
        "source": "Jim Rohn",
    },
    {
        "quote": "You are confined only by the walls you build yourself.",
        "source": "Andrew Murphy",
    },
    {
        "quote": "You've got to be in it to win it.",
        "source": "Unknown",
    },
    {
        "quote": "Every strike brings me closer to the next home run.",
        "source": "Babe Ruth",
    },
    {
        "quote": "I didn't fail the test. I just found 100 ways to do it wrong.",
        "source": "Benjamin Franklin",
    },
    {
        "quote": "If you're going through hell, keep going.",
        "source": "Winston Churchill",
    },
    {
        "quote": "Champions aren't made in the gyms. Champions are made from something they have deep inside them — a desire, a dream, a vision.",
        "source": "Muhammad Ali",
    },
    {
        "quote": "I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'",
        "source": "Muhammad Ali",
    },
    {
        "quote": "Float like a butterfly, sting like a bee.",
        "source": "Muhammad Ali",
    },
    {
        "quote": "The greatest teacher, failure is.",
        "source": "Yoda, Star Wars: The Last Jedi (2017)",
    },
    {
        "quote": "Do or do not. There is no try.",
        "source": "Yoda, Star Wars: The Empire Strikes Back (1980)",
    },
    {
        "quote": "Why do we fall? So that we can learn to pick ourselves up.",
        "source": "Alfred Pennyworth, Batman Begins (2005)",
    },
    {
        "quote": "With great power comes great responsibility.",
        "source": "Uncle Ben, Spider-Man (2002)",
    },
    {
        "quote": "You can't live your life for other people. You've got to do what's right for you, even if it hurts some people you love.",
        "source": "Nicholas Sparks, The Notebook",
    },
    {
        "quote": "After all this time? Always.",
        "source": "Severus Snape / J.K. Rowling, Harry Potter and the Deathly Hallows",
    },
    {
        "quote": "Not all treasure is silver and gold, mate.",
        "source": "Jack Sparrow, Pirates of the Caribbean (2003)",
    },
    {
        "quote": "To the well-organized mind, death is but the next great adventure.",
        "source": "Albus Dumbledore / J.K. Rowling, Harry Potter and the Sorcerer's Stone",
    },
    {
        "quote": "If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals.",
        "source": "Sirius Black / J.K. Rowling, Harry Potter and the Goblet of Fire",
    },
    {
        "quote": "The thing about failing is that it can be the first step to something incredible.",
        "source": "Brené Brown, podcast interview",
    },
    {
        "quote": "Vulnerability is not winning or losing; it's having the courage to show up and be seen when we have no control over the outcome.",
        "source": "Brené Brown, Daring Greatly",
    },
    {
        "quote": "Authenticity is the daily practice of letting go of who we think we're supposed to be and embracing who we are.",
        "source": "Brené Brown, The Gifts of Imperfection",
    },
    {
        "quote": "I'm not afraid of death; I just don't want to be there when it happens.",
        "source": "Woody Allen",
    },
    {
        "quote": "The journey of a thousand miles begins with one step.",
        "source": "Lao Tzu, Tao Te Ching",
    },
    {
        "quote": "He who knows others is wise. He who knows himself is enlightened.",
        "source": "Lao Tzu, Tao Te Ching",
    },
    {
        "quote": "Life shrinks or expands in proportion to one's courage.",
        "source": "Anais Nin",
    },
    {
        "quote": "The way to get started is to quit talking and begin doing.",
        "source": "Walt Disney",
    },
    {
        "quote": "Real courage is when you know you're licked before you begin, but you begin anyway and see it through no matter what.",
        "source": "Harper Lee, To Kill a Mockingbird",
    },
    {
        "quote": "It's not enough to be busy; so too are the ants. The question is: What are we busy about?",
        "source": "Henry David Thoreau",
    },
    {
        "quote": "The only person you should try to be better than is the person you were yesterday.",
        "source": "Matty Mullins",
    },
    {
        "quote": "No matter how hard the past, you can always begin again.",
        "source": "Buddha",
    },
    {
        "quote": "It always seems impossible until it's done.",
        "source": "Nelson Mandela",
    },
    {
        "quote": "Strength does not come from physical capacity. It comes from an indomitable will.",
        "source": "Mahatma Gandhi",
    },
    {
        "quote": "The world is changed by your example, not by your opinion.",
        "source": "Paulo Coelho",
    },
    {
        "quote": "The more you praise and celebrate your life, the more there is in life to celebrate.",
        "source": "Oprah Winfrey",
    },
    {
        "quote": "Turn your wounds into wisdom.",
        "source": "Oprah Winfrey",
    },
    {
        "quote": "Create the highest, grandest vision possible for your life, because you become what you believe.",
        "source": "Oprah Winfrey",
    },
]


def get_todays_quote():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    index = day_of_year % len(QUOTES)
    return QUOTES[index]


def send_email(quote_data, recipient_email, sender_email, app_password):
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")

    subject = f"Your Morning Fuel — {today}"

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      font-family: 'Georgia', serif;
    }}
    .wrapper {{
      max-width: 620px;
      margin: 40px auto;
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}
    .header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      padding: 40px 40px 30px;
      text-align: center;
    }}
    .header .day-label {{
      color: #e94560;
      font-size: 12px;
      font-weight: bold;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .header h1 {{
      color: #ffffff;
      font-size: 22px;
      font-weight: normal;
      margin: 0;
      letter-spacing: 1px;
    }}
    .body {{
      padding: 50px 40px;
    }}
    .quote-mark {{
      font-size: 80px;
      line-height: 0.5;
      color: #e94560;
      font-family: Georgia, serif;
      margin-bottom: 10px;
      display: block;
    }}
    .quote-text {{
      font-size: 22px;
      line-height: 1.65;
      color: #1a1a2e;
      font-style: italic;
      margin: 0 0 28px;
    }}
    .divider {{
      width: 50px;
      height: 3px;
      background: linear-gradient(to right, #e94560, #0f3460);
      margin-bottom: 20px;
      border: none;
    }}
    .source {{
      font-size: 14px;
      color: #666;
      font-style: normal;
      letter-spacing: 0.5px;
    }}
    .source strong {{
      color: #1a1a2e;
    }}
    .footer {{
      background: #f9f9f9;
      padding: 20px 40px;
      text-align: center;
      border-top: 1px solid #eee;
      font-size: 12px;
      color: #aaa;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="day-label">Good Morning</div>
      <h1>{today}</h1>
    </div>
    <div class="body">
      <span class="quote-mark">&ldquo;</span>
      <p class="quote-text">{quote_data['quote']}</p>
      <hr class="divider">
      <p class="source">— <strong>{quote_data['source']}</strong></p>
    </div>
    <div class="footer">
      Your daily dose of inspiration &bull; Go make today count.
    </div>
  </div>
</body>
</html>
"""

    plain_body = f"""Good Morning — {today}

"{quote_data['quote']}"

— {quote_data['source']}

Go make today count.
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"Quote sent to {recipient_email}: \"{quote_data['quote']}\"")


if __name__ == "__main__":
    recipient = os.environ["RECIPIENT_EMAIL"]
    sender = os.environ["GMAIL_SENDER_EMAIL"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    quote = get_todays_quote()
    send_email(quote, recipient, sender, password)
