# Slack custom emoji constraints

Source: <https://slack.com/help/articles/206870177-Add-custom-emoji-and-aliases-to-your-workspace>
Verified 2026-09-01. Re-verify before trusting these numbers in a year.

## What Slack actually enforces

| Constraint | Slack's wording | Enforced as |
|---|---|---|
| File size | "Square images under 128KB" | error above 131072 bytes |
| Format | "JPG, PNG, or GIF format" | error on anything else |
| Animation | "GIFs can include up to 50 frames" | error above 50 frames |
| Shape | "Square images ... work best" | warning — Slack scales non-square |
| Background | "transparent backgrounds work best" | not checked |
| Name | must be unique in the workspace | error on collision within `Emojis/` |

Slack does not publish a required pixel dimension. 128x128 is the practical
target because that is the resolution Slack serves to retina clients; anything
smaller upscales visibly.

## Failure catalogue

**`not a readable image`** — the bytes aren't a real PNG/JPEG/GIF regardless of
what the extension claims. Most often an SVG (vector, which Slack cannot accept
in any form) or an HTML error page saved with an image extension after a failed
download.

**`format X is not allowed`** — decodable, but a format Slack rejects (WEBP and
BMP are the usual culprits). Convert to PNG.

**`file is N KB`** — over 128 KB. For stills, downscale to 128x128 with
`optimize=True`. For GIFs, the frame count dominates the file size, so drop
frames before dropping resolution.

**`N frames`** — over Slack's 50-frame ceiling. Sample every Nth frame rather
than truncating, or the animation ends mid-loop.

**`name is not lowercase snake_case`** — only fires when the name reduces to
nothing after sanitizing (e.g. a name that was entirely punctuation or
non-Latin characters). `sanitize_name` handles ordinary spaces, hyphens, and
capitals on its own.

**`git tracks X but the file on disk is Y`** — the case-only rename bug. See
Gotchas in `SKILL.md`. This is a repository-consistency failure, not a problem
with the image itself.

## Why the validator uses Pillow

Header parsing for PNG/JPEG/GIF was hand-rolled originally and it was a large
amount of fragile struct-unpacking for something Pillow does in one call.
Pillow is a real dependency of the package for this reason — `Image.open`
gives format, dimensions, and `n_frames` uniformly across all three formats.
