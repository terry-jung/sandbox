#!/bin/bash
# Wrapper script for daily quote cron job
# Loads credentials and runs the quote emailer

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load app password from file if set
if [ -f "$SCRIPT_DIR/.gmail_app_password" ]; then
    export GMAIL_APP_PASSWORD="$(cat "$SCRIPT_DIR/.gmail_app_password")"
fi

/usr/local/bin/python3 "$SCRIPT_DIR/send_daily_quote.py" >> "$SCRIPT_DIR/quote.log" 2>&1
