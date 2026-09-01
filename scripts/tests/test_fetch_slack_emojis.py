import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fetch_slack_emojis import existing_emoji_names, resolve_aliases


def test_resolve_aliases_direct_url():
    emoji = {"parrot": "https://emoji.slack-edge.com/T000/parrot/abc.gif"}
    assert resolve_aliases(emoji) == emoji


def test_resolve_aliases_follows_chain():
    emoji = {
        "real": "https://emoji.slack-edge.com/T000/real/abc.png",
        "alias1": "alias:real",
        "alias2": "alias:alias1",
    }
    resolved = resolve_aliases(emoji)
    assert resolved["alias1"] == emoji["real"]
    assert resolved["alias2"] == emoji["real"]


def test_resolve_aliases_drops_broken_and_circular():
    emoji = {
        "dangling": "alias:missing",
        "loop_a": "alias:loop_b",
        "loop_b": "alias:loop_a",
    }
    resolved = resolve_aliases(emoji)
    assert resolved == {}


def test_existing_emoji_names(tmp_path):
    (tmp_path / "foo.png").write_bytes(b"data")
    (tmp_path / "bar.gif").write_bytes(b"data")
    assert existing_emoji_names(tmp_path) == {"foo", "bar"}


def test_existing_emoji_names_missing_dir(tmp_path):
    assert existing_emoji_names(tmp_path / "nope") == set()
