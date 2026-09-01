#!/usr/bin/env python3
"""Download all custom emojis from a Slack workspace into Emojis/."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

SLACK_API_URL = "https://slack.com/api/emoji.list"
ALIAS_PREFIX = "alias:"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "Emojis"


def fetch_emoji_list(token: str) -> dict[str, str]:
    request = urllib.request.Request(
        SLACK_API_URL,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read())
    except urllib.error.URLError as error:
        raise RuntimeError(f"Failed to reach Slack API: {error}") from error

    if not payload.get("ok"):
        error = payload.get("error", "unknown_error")
        raise RuntimeError(f"Slack API returned an error: {error}. Verify the token has the emoji:read scope.")

    return payload["emoji"]


def resolve_aliases(emoji: dict[str, str]) -> dict[str, str]:
    """Follow alias chains so every name maps to a real image URL."""
    resolved: dict[str, str] = {}
    for name, value in emoji.items():
        seen = {name}
        current = value
        while current.startswith(ALIAS_PREFIX):
            target = current[len(ALIAS_PREFIX) :]
            if target in seen or target not in emoji:
                current = None
                break
            seen.add(target)
            current = emoji[target]
        if current:
            resolved[name] = current
    return resolved


def existing_emoji_names(dest: Path) -> set[str]:
    if not dest.is_dir():
        return set()
    return {path.stem for path in dest.iterdir() if path.is_file()}


def download_emoji(name: str, url: str, dest: Path) -> Path:
    extension = Path(urlparse(url).path).suffix or ".png"
    target = dest / f"{name}{extension}"
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request, timeout=30) as response:
        target.write_bytes(response.read())
    return target


def run_update_readme() -> None:
    import runpy

    sys.argv = ["update_emojis.py"]
    runpy.run_path(str(REPO_ROOT / "scripts" / "update_emojis.py"), run_name="__main__")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--token",
        default=os.environ.get("SLACK_TOKEN"),
        help="Slack token with the emoji:read scope (defaults to $SLACK_TOKEN)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="Directory to download emojis into (default: ./Emojis)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download emojis even if a file with that name already exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be downloaded without writing any files",
    )
    parser.add_argument(
        "--skip-readme",
        action="store_true",
        help="Don't regenerate README.md after downloading",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Seconds to sleep between downloads (default: 0.1)",
    )
    args = parser.parse_args()

    if not args.token:
        parser.error("No Slack token provided. Pass --token or set SLACK_TOKEN to a token with the emoji:read scope.")

    print("Fetching emoji list from Slack...")
    emoji = fetch_emoji_list(args.token)
    resolved = resolve_aliases(emoji)
    alias_count = sum(1 for v in emoji.values() if v.startswith(ALIAS_PREFIX))
    print(f"Found {len(emoji)} emojis ({alias_count} aliases resolved).")

    args.dest.mkdir(parents=True, exist_ok=True)
    existing = existing_emoji_names(args.dest)

    downloaded, skipped, failed = 0, 0, 0
    for name, url in sorted(resolved.items()):
        if name in existing and not args.force:
            skipped += 1
            continue

        if args.dry_run:
            print(f"would download: {name}")
            downloaded += 1
            continue

        try:
            target = download_emoji(name, url, args.dest)
            print(f"downloaded: {target.relative_to(REPO_ROOT)}")
            downloaded += 1
        except (urllib.error.URLError, OSError) as error:
            print(f"failed: {name} ({error})", file=sys.stderr)
            failed += 1

        time.sleep(args.delay)

    print(f"\nDone. downloaded={downloaded} skipped={skipped} failed={failed}")

    if downloaded and not args.dry_run and not args.skip_readme:
        print("Regenerating README.md...")
        run_update_readme()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
