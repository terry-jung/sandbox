#!/bin/bash

QUOTES_FILE="/home/user/sandbox/quotes.txt"
TOTAL=$(wc -l < "$QUOTES_FILE")
DAY_OF_YEAR=$(date +%j | sed 's/^0*//')
LINE=$(( (DAY_OF_YEAR % TOTAL) + 1 ))
QUOTE=$(sed -n "${LINE}p" "$QUOTES_FILE")
DATE=$(date "+%A, %B %d")

if command -v notify-send &>/dev/null; then
  notify-send --urgency=normal --expire-time=30000 "Daily Inspiration" "$QUOTE"
fi

echo "---" >> /home/user/daily-quote.log
echo "$DATE" >> /home/user/daily-quote.log
echo "$QUOTE" >> /home/user/daily-quote.log
echo "" >> /home/user/daily-quote.log

echo ""
echo "======================================"
echo "  YOUR DAILY QUOTE -- $DATE"
echo "======================================"
echo ""
echo "$QUOTE"
echo ""
