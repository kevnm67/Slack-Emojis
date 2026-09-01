#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EMOJI_IMAGE_WIDTH = 28


def sanitize_name(stem: str) -> str:
    # Lowercase, spaces/hyphens -> underscores, strip anything else non-alnum/underscore
    slug = stem.lower()
    slug = re.sub(r"[\s-]+", "_", slug)
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug


def get_emoji_list():
    # Get a sorted list of emojis found in the Emojis directory, renaming any
    # file in place whose name isn't already lowercase snake_case.
    path = os.path.join(REPO_ROOT, "Emojis")
    files = os.listdir(path)

    renamed = []
    for filename in files:
        stem, ext = os.path.splitext(filename)
        sanitized = sanitize_name(stem) + ext.lower()
        if sanitized != filename:
            rename_emoji_file(path, filename, sanitized)
        renamed.append(sanitized)

    return sorted(renamed)


def rename_emoji_file(directory, old_name, new_name):
    """Rename an emoji file, forcing case-only renames to actually take effect.

    macOS and Windows use case-insensitive filesystems, where renaming
    "Example.png" to "example.png" is a no-op that git does not record — leaving the
    repo tracking the old capitalization while the generated README references
    the new one. On GitHub, which is case-sensitive, that renders as a broken
    image. Routing through a temporary name makes the change real on every
    platform.
    """
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)

    if old_name.lower() == new_name.lower():
        temp_path = os.path.join(directory, f"{new_name}.tmp-rename")
        os.rename(old_path, temp_path)
        os.rename(temp_path, new_path)
    else:
        os.rename(old_path, new_path)


def generate_readme(table):
    # Regerate the README.md file with the updated emoji table
    readme_path = os.path.join(REPO_ROOT, "README.md")

    with open(readme_path) as file:
        current_readme = file.read()

    emoji_heading = "## Emojis\n\n"
    next_heading = "## Attribution"
    head = current_readme.split(emoji_heading)[0]
    tail = current_readme.split(next_heading)[1]

    replacement = emoji_heading
    replacement += table + "\n\n"
    replacement += next_heading
    updated_readme = head + replacement + tail

    return updated_readme


def generate_table():
    table = []
    table.append("| Emoji              | Preview |")
    table.append("| ------------------ | ------- |")

    for emoji in get_emoji_list():
        name = emoji.split(".")[0]
        img = f'<img src="./Emojis/{emoji}" alt="{name}" width="{EMOJI_IMAGE_WIDTH}">'
        entry = f"| {name} | {img} |"
        table.append(entry)

    return "\n".join(table)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate the emoji table in README.md")
    parser.add_argument(
        "--dry-run",
        help="Print updated readme to console",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    readme = generate_readme(generate_table())
    readme_path = os.path.join(REPO_ROOT, "README.md")

    if args.dry_run:
        print(readme)
    else:
        with open(readme_path, "w") as file:
            file.write(readme)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
