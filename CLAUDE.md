# Slack-Emojis

A collection of custom emoji images plus small Python utilities to maintain
them. Personal public repo — no ticket tracker, no CI beyond GitHub Actions.

## Layout

```text
Emojis/                       the collection (lowercase snake_case filenames)
src/slack_emojis/             the package
  update_emojis.py            sanitizes filenames, regenerates the README table
  fetch_slack_emojis.py       pulls custom emoji from a Slack workspace
  emoji_spec.py               validates images against Slack's constraints
tests/                        pytest suite, mirrors src/
.claude/skills/emoji-authoring/   the skill for adding emoji
.claude/agents/emoji-curator.md   read-only pre-PR auditor
```

## Commands

```bash
make setup   # venv + editable install + pre-commit hooks
make test    # pytest
make lint    # ruff check
make build   # regenerate README.md from Emojis/
make ci      # lint + test + build, what CI runs
python -m slack_emojis.emoji_spec --audit    # validate the whole collection
```

## Rules for this repo

- **The README emoji table is generated. Never hand-edit it.** Run `make build`
  and commit the result. Editing it by hand produces a diff that the next
  generator run silently reverts.
- **Adding an emoji goes through the `emoji-authoring` skill.** It exists so
  the validate → place → regenerate → audit sequence actually happens in order.
- **Case-only renames need two `git mv` calls.** macOS is case-insensitive, so
  `git mv X.png x.png` records nothing and GitHub ends up serving a broken
  image. Go through a temp name. `rename_emoji_file()` does this correctly in
  code; the manual fix is
  `git mv Emojis/X.png Emojis/tmp && git mv Emojis/tmp Emojis/x.png`.
- **Non-square emoji are fine.** Slack scales them. 31 in the collection are
  non-square. The validator reports them as warnings, not errors — don't
  "fix" them unprompted.
- **`SLACK_TOKEN` is a user token (`xoxp-`), not a bot token.** `emoji.list`
  requires the `emoji:read` user scope. Resolve it with `op read`, never paste
  it into a file or the terminal.
- **Python is pinned to 3.14** via `.python-version` and `requires-python`.

## Before opening a PR

`make ci` must pass, and `python -m slack_emojis.emoji_spec --audit` must
report zero failures. CI runs both, plus a `ruff format --check`.
