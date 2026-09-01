#!/usr/bin/env python3
"""Validate emoji images against Slack's custom-emoji constraints.

Slack's published limits (verified 2026-09-01 against
https://slack.com/help/articles/206870177): under 128 KB, JPG/PNG/GIF only,
GIFs limited to 50 frames, square images recommended.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from slack_emojis.update_emojis import REPO_ROOT, sanitize_name

MAX_BYTES = 128 * 1024
MAX_GIF_FRAMES = 50
ALLOWED_FORMATS = {"PNG", "JPEG", "GIF"}
RECOMMENDED_EDGE = 128
VALID_NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
EMOJI_DIR = REPO_ROOT / "Emojis"
PROVENANCE_FILE = REPO_ROOT / "provenance.json"

# Substrings suggesting third-party IP. Deliberately a heuristic prompting a
# human look, not a copyright determination — it cannot make one.
BRAND_HINTS = frozenset(
    {
        "apple",
        "aws",
        "azure",
        "circleci",
        "datadog",
        "disney",
        "figma",
        "github",
        "grafana",
        "hashicorp",
        "jira",
        "kong",
        "linkedin",
        "marvel",
        "mario",
        "luigi",
        "netflix",
        "nintendo",
        "pokemon",
        "postman",
        "salesforce",
        "sentry",
        "slack",
        "starwars",
        "terraform",
        "vscode",
        "xcode",
        "zoom",
        # characters and people
        "bob_ross",
        "carlton",
        "devito",
        "fry",
        "ghostbusters",
        "homer",
        "johnwick",
        "keanu",
        "mrburns",
        "ralph",
        "simpson",
        "wick",
    }
)


@dataclass
class Report:
    """Outcome of validating one emoji."""

    path: str
    name: str
    image_format: str | None = None
    size: tuple[int, int] | None = None
    size_bytes: int | None = None
    frames: int | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    copyright_notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate(
    path: Path, name: str | None = None, existing: set[str] | None = None
) -> Report:
    """Validate one image, collecting every violation rather than the first."""
    report = Report(path=str(path), name=sanitize_name(name if name else path.stem))

    if not path.is_file():
        report.errors.append(f"file does not exist: {path}")
        return report

    report.size_bytes = path.stat().st_size

    try:
        with Image.open(path) as image:
            report.image_format = image.format
            report.size = image.size
            report.frames = getattr(image, "n_frames", 1)
    except UnidentifiedImageError:
        report.errors.append(
            f"not a readable image ({path.suffix} is not a real PNG/JPEG/GIF)"
        )
        return report

    width, height = report.size

    if report.image_format not in ALLOWED_FORMATS:
        report.errors.append(
            f"format {report.image_format} is not allowed; use PNG/JPEG/GIF"
        )
    if report.size_bytes > MAX_BYTES:
        report.errors.append(
            f"file is {report.size_bytes / 1024:.1f} KB; Slack's limit is 128 KB"
        )
    if report.frames > MAX_GIF_FRAMES:
        report.errors.append(
            f"{report.frames} frames; Slack allows at most {MAX_GIF_FRAMES}"
        )
    if not VALID_NAME.match(report.name):
        report.errors.append(f"name {report.name!r} is not lowercase snake_case")
    if existing and report.name in existing:
        report.errors.append(f"an emoji named {report.name!r} already exists")

    # Slack accepts non-square images and scales them, so this stays a warning.
    if width != height:
        report.warnings.append(
            f"{width}x{height} is not square; square avoids letterboxing"
        )
    elif width < RECOMMENDED_EDGE:
        report.warnings.append(
            f"{width}x{height} is below the {RECOMMENDED_EDGE}px retina size"
        )

    # Copyright signals are advisory: uploading to your own workspace is not
    # redistribution, so these only become errors under --committing.
    report.copyright_notes = check_copyright(report.name, path)

    return report


def check_copyright(name: str, path: Path) -> list[str]:
    """Flag likely third-party IP and missing provenance.

    Advisory by design: this cannot determine copyright, only surface the
    signals a human should look at. Callers decide whether these block.
    """
    notes = []

    recorded = (
        json.loads(PROVENANCE_FILE.read_text())["emoji"]
        if PROVENANCE_FILE.exists()
        else {}
    )
    if name not in recorded:
        notes.append(f"no provenance recorded for {name!r}; add it to provenance.json")

    if any(brand in name for brand in BRAND_HINTS):
        notes.append(
            f"{name!r} looks like third-party IP (brand, character, or celebrity). "
            "Fan art is generally unlicensed — fine for your own workspace, a "
            "redistribution risk in a public repo"
        )

    # PNG/JPEG can carry a copyright field; surface it rather than guessing.
    try:
        with Image.open(path) as image:
            for key in ("copyright", "Copyright", "Artist"):
                if value := (image.info or {}).get(key):
                    notes.append(f"image metadata declares {key}: {value}")
    except UnidentifiedImageError, OSError:
        pass

    return notes


def audit_tracked_names() -> list[Report]:
    """Flag emoji whose git-tracked filename differs from the name on disk.

    On case-insensitive filesystems (macOS, Windows) an emoji can sit on disk as
    "example.png" while git still tracks "Example.png". The README references the
    on-disk name, so GitHub — case-sensitive — serves a broken image.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "Emojis"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError, FileNotFoundError:
        return []  # not a git checkout

    on_disk = {p.name for p in EMOJI_DIR.iterdir() if p.is_file()}
    lowered = {n.lower(): n for n in on_disk}
    reports = []

    for entry in result.stdout.split():
        tracked = Path(entry).name
        if tracked in on_disk:
            continue
        report = Report(path=entry, name=Path(tracked).stem)
        actual = lowered.get(tracked.lower())
        report.errors.append(
            f"git tracks {tracked!r} but the file on disk is {actual!r}; GitHub is "
            "case-sensitive and will serve a broken image"
            if actual
            else f"git tracks {tracked!r} but no such file exists on disk"
        )
        reports.append(report)

    return reports


def audit_duplicate_names() -> list[Report]:
    """Flag files that collide on emoji name, e.g. claude_code.gif vs claude_code.png.

    The emoji name is the filename stem, so two files differing only by
    extension are two files claiming one Slack emoji name.
    """
    by_stem: dict[str, list[str]] = {}
    for path in EMOJI_DIR.iterdir():
        if path.is_file():
            by_stem.setdefault(sanitize_name(path.stem), []).append(path.name)

    return [
        Report(
            path=", ".join(sorted(names)),
            name=stem,
            errors=[f"{len(names)} files claim {stem!r}: {', '.join(sorted(names))}"],
        )
        for stem, names in by_stem.items()
        if len(names) > 1
    ]


def print_report(report: Report) -> None:
    print(f"{'PASS' if report.ok else 'FAIL'}  {report.name}  ({report.path})")
    for error in report.errors:
        print(f"      error:   {error}")
    for warning in report.warnings:
        print(f"      warning: {warning}")
    for note in report.copyright_notes:
        print(f"      copyright: {note}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="image file(s) to validate")
    parser.add_argument(
        "--name", help="emoji name to check (defaults to the file stem)"
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    parser.add_argument(
        "--audit", action="store_true", help="check the whole Emojis/ collection"
    )
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as failures (used in CI)"
    )
    parser.add_argument(
        "--committing",
        action="store_true",
        help="treat copyright notes as failures; use when committing here",
    )
    args = parser.parse_args()

    if args.name and len(args.paths) > 1:
        parser.error("--name only applies to a single file")
    if not args.paths and not args.audit:
        parser.error("pass at least one path, or --audit to check the whole collection")

    if args.audit:
        paths = sorted(p for p in EMOJI_DIR.iterdir() if p.is_file())
        reports = (
            [validate(p) for p in paths]
            + audit_tracked_names()
            + audit_duplicate_names()
        )
    else:
        existing = {p.stem for p in EMOJI_DIR.iterdir() if p.is_file()}
        reports = [validate(p, args.name, existing) for p in args.paths]

    if args.json:
        print(
            json.dumps(
                [vars(r) | {"ok": r.ok} for r in reports], indent=2, default=list
            )
        )
    else:
        for report in reports:
            print_report(report)
        failed = sum(1 for r in reports if not r.ok)
        print(f"\n{len(reports) - failed} passed, {failed} failed")

    failed = any(not r.ok for r in reports)
    if args.strict:
        failed = failed or any(r.warnings for r in reports)
    if args.committing:
        failed = failed or any(r.copyright_notes for r in reports)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
