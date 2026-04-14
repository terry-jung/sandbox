"""MCP server for interacting with iMessage on macOS.

Reads messages from ~/Library/Messages/chat.db and sends messages via AppleScript.
Requires macOS with Messages.app and Full Disk Access for the terminal running this server.
"""

import os
import sqlite3
import subprocess
import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

CHAT_DB_PATH = os.environ.get(
    "IMESSAGE_DB_PATH",
    str(Path.home() / "Library" / "Messages" / "chat.db"),
)

mcp = FastMCP(
    "iMessage",
    instructions=(
        "MCP server for Apple iMessage. "
        "Read conversations, search message history, and send iMessages. "
        "Requires macOS with Full Disk Access granted to the host terminal."
    ),
)


def _get_db() -> sqlite3.Connection:
    """Return a read-only connection to chat.db."""
    if not Path(CHAT_DB_PATH).exists():
        raise FileNotFoundError(
            f"iMessage database not found at {CHAT_DB_PATH}. "
            "Make sure you are running on macOS and have granted Full Disk Access."
        )
    conn = sqlite3.connect(f"file:{CHAT_DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _apple_epoch_to_iso(ns: int | None) -> str | None:
    """Convert Apple's CoreData timestamp (nanoseconds since 2001-01-01) to ISO 8601."""
    if ns is None or ns == 0:
        return None
    apple_epoch = datetime.datetime(2001, 1, 1)
    dt = apple_epoch + datetime.timedelta(seconds=ns / 1e9)
    return dt.isoformat()


# ── Tools ────────────────────────────────────────────────────────────────────


@mcp.tool()
def list_conversations(limit: int = 20) -> list[dict]:
    """List recent iMessage conversations.

    Returns conversation ID, participant phone/email, and the display name
    for each chat. Results are ordered by most recent message.

    Args:
        limit: Maximum number of conversations to return (default 20).
    """
    db = _get_db()
    try:
        rows = db.execute(
            """
            SELECT
                c.ROWID            AS chat_id,
                c.chat_identifier  AS identifier,
                c.display_name     AS display_name,
                c.service_name     AS service,
                MAX(m.date)        AS last_message_date
            FROM chat c
            LEFT JOIN chat_message_join cmj ON cmj.chat_id = c.ROWID
            LEFT JOIN message m            ON m.ROWID = cmj.message_id
            GROUP BY c.ROWID
            ORDER BY last_message_date DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [
            {
                "chat_id": row["chat_id"],
                "identifier": row["identifier"],
                "display_name": row["display_name"] or row["identifier"],
                "service": row["service"],
                "last_message": _apple_epoch_to_iso(row["last_message_date"]),
            }
            for row in rows
        ]
    finally:
        db.close()


@mcp.tool()
def read_messages(chat_id: int, limit: int = 50) -> list[dict]:
    """Read messages from a specific conversation.

    Args:
        chat_id: The conversation ID (from list_conversations).
        limit: Maximum number of messages to return (default 50, most recent first).
    """
    db = _get_db()
    try:
        rows = db.execute(
            """
            SELECT
                m.ROWID        AS message_id,
                m.text         AS text,
                m.is_from_me   AS is_from_me,
                m.date         AS date,
                m.service      AS service,
                h.id           AS sender
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            LEFT JOIN handle h         ON h.ROWID = m.handle_id
            WHERE cmj.chat_id = ?
            ORDER BY m.date DESC
            LIMIT ?
            """,
            (chat_id, limit),
        ).fetchall()

        return [
            {
                "message_id": row["message_id"],
                "text": row["text"],
                "is_from_me": bool(row["is_from_me"]),
                "sender": "me" if row["is_from_me"] else (row["sender"] or "unknown"),
                "date": _apple_epoch_to_iso(row["date"]),
                "service": row["service"],
            }
            for row in rows
        ]
    finally:
        db.close()


@mcp.tool()
def search_messages(query: str, limit: int = 30) -> list[dict]:
    """Search all iMessage history for messages containing the query text.

    Args:
        query: Text to search for (case-insensitive substring match).
        limit: Maximum number of results (default 30).
    """
    db = _get_db()
    try:
        rows = db.execute(
            """
            SELECT
                m.ROWID        AS message_id,
                m.text         AS text,
                m.is_from_me   AS is_from_me,
                m.date         AS date,
                h.id           AS sender,
                c.chat_identifier AS chat_identifier,
                c.display_name    AS chat_display_name
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            JOIN chat c                ON c.ROWID = cmj.chat_id
            LEFT JOIN handle h         ON h.ROWID = m.handle_id
            WHERE m.text LIKE ?
            ORDER BY m.date DESC
            LIMIT ?
            """,
            (f"%{query}%", limit),
        ).fetchall()

        return [
            {
                "message_id": row["message_id"],
                "text": row["text"],
                "is_from_me": bool(row["is_from_me"]),
                "sender": "me" if row["is_from_me"] else (row["sender"] or "unknown"),
                "date": _apple_epoch_to_iso(row["date"]),
                "chat": row["chat_display_name"] or row["chat_identifier"],
            }
            for row in rows
        ]
    finally:
        db.close()


@mcp.tool()
def get_contact_info(chat_id: int) -> list[dict]:
    """Get participant details for a conversation.

    Args:
        chat_id: The conversation ID (from list_conversations).
    """
    db = _get_db()
    try:
        rows = db.execute(
            """
            SELECT
                h.ROWID  AS handle_id,
                h.id     AS identifier,
                h.service AS service
            FROM handle h
            JOIN chat_handle_join chj ON chj.handle_id = h.ROWID
            WHERE chj.chat_id = ?
            """,
            (chat_id,),
        ).fetchall()

        return [
            {
                "handle_id": row["handle_id"],
                "identifier": row["identifier"],
                "service": row["service"],
            }
            for row in rows
        ]
    finally:
        db.close()


@mcp.tool()
def send_message(recipient: str, text: str, service: str = "iMessage") -> str:
    """Send an iMessage or SMS to a recipient.

    Uses AppleScript to send via the macOS Messages app.
    The Messages app must be running or will be launched automatically.

    Args:
        recipient: Phone number (e.g. +1234567890) or email address.
        text: The message body to send.
        service: "iMessage" or "SMS". Defaults to iMessage.
    """
    service_name = "SMS" if service.upper() == "SMS" else "iMessage"

    # Escape backslashes and double quotes for AppleScript string literals
    safe_text = text.replace("\\", "\\\\").replace('"', '\\"')
    safe_recipient = recipient.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = {service_name}
        set targetBuddy to buddy "{safe_recipient}" of targetService
        send "{safe_text}" to targetBuddy
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=15,
    )

    if result.returncode != 0:
        raise RuntimeError(f"AppleScript error: {result.stderr.strip()}")

    return f"Message sent to {recipient} via {service_name}."


@mcp.tool()
def count_messages(chat_id: int) -> dict:
    """Get message count statistics for a conversation.

    Args:
        chat_id: The conversation ID (from list_conversations).
    """
    db = _get_db()
    try:
        row = db.execute(
            """
            SELECT
                COUNT(*)                              AS total,
                SUM(CASE WHEN m.is_from_me = 1 THEN 1 ELSE 0 END) AS sent,
                SUM(CASE WHEN m.is_from_me = 0 THEN 1 ELSE 0 END) AS received,
                MIN(m.date)                           AS first_message,
                MAX(m.date)                           AS last_message
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            WHERE cmj.chat_id = ?
            """,
            (chat_id,),
        ).fetchone()

        return {
            "total": row["total"],
            "sent": row["sent"],
            "received": row["received"],
            "first_message": _apple_epoch_to_iso(row["first_message"]),
            "last_message": _apple_epoch_to_iso(row["last_message"]),
        }
    finally:
        db.close()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
