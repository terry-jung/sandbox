#!/usr/bin/env python3
"""Background scheduler — runs daily_quote.py every day at 10:00 AM Asia/Seoul.

Start with: nohup python3 /home/user/scripts/quote_scheduler.py > /home/user/scripts/scheduler.log 2>&1 &
"""

import time
import subprocess
import sys
import os
from datetime import datetime
import zoneinfo

TIMEZONE = zoneinfo.ZoneInfo("Asia/Seoul")
TARGET_HOUR = 10
TARGET_MINUTE = 0
SCRIPT = os.path.join(os.path.dirname(__file__), "daily_quote.py")
LOG_FILE = os.path.join(os.path.dirname(__file__), "scheduler.log")
SENT_DATES_FILE = os.path.join(os.path.dirname(__file__), ".sent_dates")

# Persist the ANTHROPIC_API_KEY so it survives re-runs
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


def load_sent_dates():
    if os.path.exists(SENT_DATES_FILE):
        with open(SENT_DATES_FILE) as f:
            return set(f.read().splitlines())
    return set()


def mark_sent(date_str):
    with open(SENT_DATES_FILE, "a") as f:
        f.write(date_str + "\n")


def log(msg):
    now = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S KST")
    line = f"[{now}] {msg}"
    print(line, flush=True)


def run_quote_script():
    env = os.environ.copy()
    if API_KEY:
        env["ANTHROPIC_API_KEY"] = API_KEY
    result = subprocess.run(
        [sys.executable, SCRIPT],
        env=env,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        log(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        log(f"ERROR: {result.stderr.strip()}")
    return result.returncode == 0


def main():
    log(f"Scheduler started. Will send daily quote at {TARGET_HOUR:02d}:{TARGET_MINUTE:02d} KST.")
    sent_dates = load_sent_dates()

    while True:
        now = datetime.now(TIMEZONE)
        today_str = now.strftime("%Y-%m-%d")

        if (
            now.hour == TARGET_HOUR
            and now.minute == TARGET_MINUTE
            and today_str not in sent_dates
        ):
            log(f"It's 10am — sending today's quote...")
            ok = run_quote_script()
            if ok:
                mark_sent(today_str)
                sent_dates.add(today_str)
            else:
                log("Failed — will retry in 5 minutes.")
                time.sleep(300)
                continue

        # Sleep until the next minute
        time.sleep(60 - datetime.now(TIMEZONE).second)


if __name__ == "__main__":
    main()
