"""YouTube MCP Server.

Provides tools to "watch" YouTube videos by fetching their metadata and
transcripts, so an LLM can summarize the content and surface key takeaways
without actually streaming the video.

Tools:
  - youtube_get_video_info: fetch title, channel, duration, description, views, etc.
  - youtube_get_transcript: fetch the full transcript (captions) of a video.
  - youtube_watch_video: one-shot convenience tool returning info + transcript together.
  - youtube_search: search YouTube for videos matching a query (no API key required).
"""

from __future__ import annotations

import os
import re
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

# youtube-transcript-api (new API uses an instance)
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

import yt_dlp


mcp = FastMCP("youtube_mcp")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(video: str) -> str:
    """Accept a raw 11-char video id OR any common YouTube URL form and
    return the canonical 11-character video id.

    Supports:
      - https://www.youtube.com/watch?v=VIDEOID
      - https://youtu.be/VIDEOID
      - https://www.youtube.com/shorts/VIDEOID
      - https://www.youtube.com/embed/VIDEOID
      - https://m.youtube.com/watch?v=VIDEOID
      - bare VIDEOID
    """
    video = video.strip()

    # Bare id
    if _VIDEO_ID_RE.match(video):
        return video

    try:
        parsed = urlparse(video)
    except Exception as e:
        raise ValueError(f"Could not parse '{video}' as a video id or URL: {e}")

    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    # youtu.be/<id>
    if host.endswith("youtu.be"):
        candidate = path.lstrip("/").split("/")[0]
        if _VIDEO_ID_RE.match(candidate):
            return candidate

    # youtube.com/watch?v=<id>
    if "youtube.com" in host:
        qs = parse_qs(parsed.query or "")
        if "v" in qs and qs["v"]:
            candidate = qs["v"][0]
            if _VIDEO_ID_RE.match(candidate):
                return candidate

        # /shorts/<id>, /embed/<id>, /v/<id>, /live/<id>
        parts = [p for p in path.split("/") if p]
        if len(parts) >= 2 and parts[0] in {"shorts", "embed", "v", "live"}:
            candidate = parts[1]
            if _VIDEO_ID_RE.match(candidate):
                return candidate

    raise ValueError(
        f"Could not extract a YouTube video id from '{video}'. "
        "Pass the 11-character video id or a standard YouTube URL."
    )


def _format_duration(seconds: Optional[int]) -> str:
    if not seconds:
        return "unknown"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def _fetch_metadata(video_id: str) -> dict[str, Any]:
    """Use yt-dlp in metadata-only mode to grab video info without downloading."""
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "video_id": video_id,
        "url": url,
        "title": info.get("title"),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_url": info.get("channel_url") or info.get("uploader_url"),
        "upload_date": info.get("upload_date"),  # YYYYMMDD
        "duration_seconds": info.get("duration"),
        "duration_human": _format_duration(info.get("duration")),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "description": info.get("description"),
        "tags": info.get("tags") or [],
        "categories": info.get("categories") or [],
        "language": info.get("language"),
        "thumbnail": info.get("thumbnail"),
    }


def _fetch_transcript(
    video_id: str, languages: list[str]
) -> tuple[str, str, bool]:
    """Fetch the transcript using the current youtube-transcript-api API.

    Returns (plain_text, language_code, is_generated).
    """
    api = YouTubeTranscriptApi()

    # list() returns a TranscriptList we can search by language preference
    transcript_list = api.list(video_id)

    # Try manually-created captions first in the requested languages,
    # then fall back to auto-generated.
    try:
        t = transcript_list.find_manually_created_transcript(languages)
    except NoTranscriptFound:
        try:
            t = transcript_list.find_generated_transcript(languages)
        except NoTranscriptFound:
            # Last resort: grab *any* transcript and translate it to the first
            # requested language if possible.
            available = list(transcript_list)
            if not available:
                raise
            t = available[0]
            if t.is_translatable and languages:
                try:
                    t = t.translate(languages[0])
                except Exception:
                    pass

    fetched = t.fetch()  # FetchedTranscript (iterable of snippets)
    # Each snippet has .text, .start, .duration
    lines = [s.text for s in fetched if getattr(s, "text", "").strip()]
    plain_text = " ".join(lines)
    # Collapse whitespace / newlines inside captions
    plain_text = re.sub(r"\s+", " ", plain_text).strip()
    return plain_text, t.language_code, t.is_generated


# ---------------------------------------------------------------------------
# Tool: get_video_info
# ---------------------------------------------------------------------------

class VideoInfoInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )
    video: str = Field(
        ...,
        description=(
            "YouTube video URL or 11-character video id. "
            "Examples: 'https://youtu.be/dQw4w9WgXcQ', "
            "'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'."
        ),
        min_length=1,
        max_length=500,
    )


@mcp.tool(
    name="youtube_get_video_info",
    annotations={
        "title": "Get YouTube Video Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def youtube_get_video_info(params: VideoInfoInput) -> dict[str, Any]:
    """Fetch metadata for a YouTube video: title, channel, duration, views,
    upload date, description, and tags. Does not fetch the transcript.
    """
    try:
        video_id = extract_video_id(params.video)
    except ValueError as e:
        return {"error": str(e)}

    try:
        meta = _fetch_metadata(video_id)
    except Exception as e:
        return {
            "error": f"Failed to fetch metadata for video {video_id}: {e}",
            "video_id": video_id,
            "hint": "The video may be private, deleted, age-restricted, or region-blocked.",
        }

    return meta


# ---------------------------------------------------------------------------
# Tool: get_transcript
# ---------------------------------------------------------------------------

class TranscriptInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )
    video: str = Field(
        ...,
        description="YouTube video URL or 11-character video id.",
        min_length=1,
        max_length=500,
    )
    languages: list[str] = Field(
        default_factory=lambda: ["en", "ko"],
        description=(
            "Preferred caption languages in priority order, as BCP-47 / ISO-639-1 codes. "
            "Defaults to ['en', 'ko']. The server will try manually-created captions "
            "first, then auto-generated, then any available translated to the first code."
        ),
        max_length=10,
    )


@mcp.tool(
    name="youtube_get_transcript",
    annotations={
        "title": "Get YouTube Video Transcript",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def youtube_get_transcript(params: TranscriptInput) -> dict[str, Any]:
    """Fetch the transcript (captions) of a YouTube video as plain text.

    Tries manually-created captions first in the preferred languages, then
    auto-generated captions, then any available captions translated to the
    first preferred language.
    """
    try:
        video_id = extract_video_id(params.video)
    except ValueError as e:
        return {"error": str(e)}

    try:
        text, lang, is_generated = _fetch_transcript(video_id, params.languages)
    except TranscriptsDisabled:
        return {
            "error": "Transcripts are disabled for this video.",
            "video_id": video_id,
        }
    except NoTranscriptFound:
        return {
            "error": f"No transcript found in any of the requested languages: {params.languages}.",
            "video_id": video_id,
            "hint": "Try different language codes or call youtube_get_video_info to see the video's language.",
        }
    except VideoUnavailable:
        return {
            "error": "Video is unavailable (may be private, deleted, or region-blocked).",
            "video_id": video_id,
        }
    except Exception as e:
        return {"error": f"Failed to fetch transcript: {e}", "video_id": video_id}

    return {
        "video_id": video_id,
        "language": lang,
        "is_auto_generated": is_generated,
        "character_count": len(text),
        "word_count": len(text.split()),
        "transcript": text,
    }


# ---------------------------------------------------------------------------
# Tool: watch_video (convenience: info + transcript in one call)
# ---------------------------------------------------------------------------

class WatchInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )
    video: str = Field(
        ...,
        description="YouTube video URL or 11-character video id.",
        min_length=1,
        max_length=500,
    )
    languages: list[str] = Field(
        default_factory=lambda: ["en", "ko"],
        description="Preferred transcript languages. Defaults to ['en', 'ko'].",
        max_length=10,
    )


@mcp.tool(
    name="youtube_watch_video",
    annotations={
        "title": "Watch YouTube Video (info + transcript)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def youtube_watch_video(params: WatchInput) -> dict[str, Any]:
    """One-shot tool: fetch both video metadata and transcript. Use this when
    you want to summarize a video — it gives the model everything it needs in
    a single tool call.
    """
    try:
        video_id = extract_video_id(params.video)
    except ValueError as e:
        return {"error": str(e)}

    result: dict[str, Any] = {"video_id": video_id}

    # Metadata
    try:
        result["info"] = _fetch_metadata(video_id)
    except Exception as e:
        result["info_error"] = f"Failed to fetch metadata: {e}"

    # Transcript
    try:
        text, lang, is_generated = _fetch_transcript(video_id, params.languages)
        result["transcript"] = {
            "language": lang,
            "is_auto_generated": is_generated,
            "character_count": len(text),
            "word_count": len(text.split()),
            "text": text,
        }
    except TranscriptsDisabled:
        result["transcript_error"] = "Transcripts are disabled for this video."
    except NoTranscriptFound:
        result["transcript_error"] = (
            f"No transcript in any of {params.languages}. Try other language codes."
        )
    except VideoUnavailable:
        result["transcript_error"] = "Video is unavailable."
    except Exception as e:
        result["transcript_error"] = f"Failed to fetch transcript: {e}"

    return result


# ---------------------------------------------------------------------------
# Tool: search
# ---------------------------------------------------------------------------

class SearchInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )
    query: str = Field(
        ...,
        description="Search query, e.g. 'quantum computing explained'.",
        min_length=1,
        max_length=500,
    )
    max_results: int = Field(
        default=5,
        description="Maximum number of results to return (1-20).",
        ge=1,
        le=20,
    )


@mcp.tool(
    name="youtube_search",
    annotations={
        "title": "Search YouTube",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,  # ranking can change
        "openWorldHint": True,
    },
)
async def youtube_search(params: SearchInput) -> dict[str, Any]:
    """Search YouTube for videos matching a query. Returns a list of results
    with id, title, channel, duration, and URL. Does NOT require an API key.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "extract_flat": True,
        "default_search": "ytsearch",
    }
    search_url = f"ytsearch{params.max_results}:{params.query}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
    except Exception as e:
        return {"error": f"Search failed: {e}", "query": params.query}

    entries = info.get("entries") or []
    results = []
    for e in entries:
        if not e:
            continue
        vid = e.get("id")
        results.append(
            {
                "video_id": vid,
                "title": e.get("title"),
                "channel": e.get("channel") or e.get("uploader"),
                "duration_seconds": e.get("duration"),
                "duration_human": _format_duration(e.get("duration")),
                "view_count": e.get("view_count"),
                "url": f"https://www.youtube.com/watch?v={vid}" if vid else None,
            }
        )

    return {"query": params.query, "count": len(results), "results": results}


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
