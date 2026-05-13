#!/bin/bash

export PATH="/opt/node22/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

PROMPT='Pick one aspirational, inspirational, positive quote that will help someone feel pumped and ready to take on the day. The quote can be from a movie, book, speech, article, interview, conversation, song, or podcast — anything goes. Then send it to me via KakaoTalk using the KakaotalkChat-MemoChat tool. Format the message like this:

Good morning! Here is your quote for today:

"[quote]"
— [who said it / source]

Keep it under 200 characters total.'

/opt/node22/bin/claude \
  --dangerously-skip-permissions \
  -p "$PROMPT" \
  >> /home/user/sandbox/daily_quote.log 2>&1
