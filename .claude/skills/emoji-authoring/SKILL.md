---
name: emoji-authoring
description: >
  Add, validate, or fix custom emoji images in this repository's Emojis/
  collection. Use when the user wants to add a new emoji, drops an image file
  in and wants it turned into a Slack emoji, asks why an emoji looks broken or
  isn't showing up in the README, wants emoji filenames cleaned up, or asks to
  check whether the emoji set is still valid — even if they don't say "emoji
  spec", "validate", or name the Emojis/ directory directly. Also use when
  converting an image to Slack's required format (square, under 128 KB,
  PNG/JPEG/GIF, 50-frame GIF limit).
license: MIT
compatibility: Requires Python 3.14+, an editable install of this repo (make setup), and rsvg-convert for SVG conversion
allowed-tools: Bash(python:*) Bash(make:*) Bash(git:*) Bash(rsvg-convert:*) Read Write Edit Glob
---

# Emoji authoring

Adding an emoji is a fixed pipeline. Run the scripts — do not eyeball image
dimensions or hand-edit the README table.

## Workflow

- [ ] 1. Validate the candidate: `python -m slack_emojis.emoji_spec <file> --name <name>`
- [ ] 2. Fix anything it reports (see Fixing failures below), re-run until it passes
- [ ] 3. Move the file into `Emojis/` under its sanitized name
- [ ] 4. Regenerate the README: `make build`
- [ ] 5. Audit the whole collection: `python -m slack_emojis.emoji_spec --audit`
- [ ] 6. Confirm `git status` shows the new file *and* the README change

Step 5 is not optional. It is the only check that catches the case-rename bug
in Gotchas below, and it is what CI runs.

## Slack's constraints

| Rule | Value |
|---|---|
| Max file size | 128 KB (hard failure) |
| Formats | PNG, JPEG, GIF only (hard failure) |
| GIF frames | 50 max (hard failure) |
| Shape | Square recommended, non-square accepted (warning) |
| Size | 128x128 for retina sharpness (warning below that) |
| Name | lowercase snake_case, auto-sanitized |

Verified 2026-09-01 against <https://slack.com/help/articles/206870177>. Full
details and the failure catalogue: [references/slack-constraints.md](references/slack-constraints.md).

## Fixing failures

**Not a PNG/JPEG/GIF (e.g. an SVG).** Slack cannot upload vector files at all.
Convert, then delete the original:

```bash
rsvg-convert -w 128 -h 128 input.svg -o Emojis/name.png
git rm Emojis/name.svg
```

**Over 128 KB.** Downscale to 128x128 first; that alone usually clears it:

```bash
python -c "from PIL import Image; i=Image.open('in.png'); i.thumbnail((128,128)); i.save('out.png', optimize=True)"
```

For an oversize GIF, drop frames rather than resolution — frame count drives
the size.

**Name rejected.** `sanitize_name` already lowercases and converts separators
to underscores. A rejection means the name is empty after stripping invalid
characters — pick a real name rather than fighting the sanitizer.

## Gotchas

- **A case-only rename silently does nothing on macOS.** `DOPS.png` →
  `dops.png` succeeds on disk but git records no change, so git keeps tracking
  `DOPS.png` while the generated README points at `dops.png`. GitHub is
  case-sensitive, so it renders as a broken image with no local symptom.
  `rename_emoji_file()` routes through a temp name to prevent this; if you hit
  it on an existing file, fix it with two moves:
  `git mv Emojis/X.png Emojis/tmp && git mv Emojis/tmp Emojis/x.png`.
- **Never hand-edit the emoji table in README.md.** It is generated. Run
  `make build` and commit the result.
- **`get_emoji_list()` renames files as a side effect of reading them.** Just
  running the README generator will sanitize filenames on disk.
- **Non-square is a warning, not an error.** 31 emoji in the collection are
  non-square and render fine. Don't "fix" them unless asked.
- **Validation reports every problem at once**, not just the first — read the
  whole list before editing.

## Adding several at once

Validate the batch before moving anything, so a bad file doesn't land
half-committed:

```bash
python -m slack_emojis.emoji_spec ~/Downloads/*.png --json
```

Then move the ones that passed, run `make build` once, and audit.
