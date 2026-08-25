#!/usr/bin/env python3
"""Beatport Downloader PRO — Lightweight CLI Companion Client
Query Beatport catalog metadata, verify Camelot keys, and inspect lossless audio quality.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

API_BASE_URL = "https://beatport-downloader.com/api"

def search_tracks(query: str, limit: int = 10):
    params = urllib.parse.urlencode({"q": query, "limit": limit})
    url = f"{API_BASE_URL}/search?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "BeatportCLI/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("tracks", [])
    except Exception as e:
        print(f"Error communicating with Beatport Downloader API: {e}", file=sys.stderr)
        return []

def print_track_table(tracks):
    if not tracks:
        print("No tracks found.")
        return
    print("\n" + "=" * 90)
    print(f"{'#':<3} | {'TITLE':<30} | {'ARTIST':<22} | {'BPM':<6} | {'KEY':<5} | {'LABEL':<16}")
    print("=" * 90)
    for idx, t in enumerate(tracks, 1):
        title = (t.get("title", "") + " (" + t.get("mix_name", "Original Mix") + ")")[:30]
        artist = t.get("artist", "Unknown")[:22]
        bpm = str(t.get("bpm", "—"))[:6]
        key = str(t.get("camelot_key", t.get("key_name", "—")))[:5]
        label = t.get("label", "Independent")[:16]
        print(f"{idx:<3} | {title:<30} | {artist:<22} | {bpm:<6} | {key:<5} | {label:<16}")
    print("=" * 90 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Beatport Downloader PRO — Catalog Search & Metadata Inspector")
    parser.add_argument("query", nargs="*", help="Track title, artist name, or genre query")
    parser.add_argument("--limit", type=int, default=10, help="Max results to display (default: 10)")
    args = parser.parse_args()

    q = " ".join(args.query).strip() if args.query else "Melodic Techno"
    print(f"Searching Beatport catalog for: '{q}'...")
    tracks = search_tracks(q, limit=args.limit)
    print_track_table(tracks)
    print("To download bit-perfect 24-bit FLAC files with full ID3 tags, visit: https://beatport-downloader.com")

if __name__ == "__main__":
    main()
