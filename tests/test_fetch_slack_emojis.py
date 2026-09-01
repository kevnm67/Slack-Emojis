import json
from io import BytesIO
from unittest.mock import patch

from slack_emojis.fetch_slack_emojis import (
    download_emoji,
    existing_emoji_names,
    fetch_emoji_list,
    resolve_aliases,
)


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


class _FakeResponse:
    def __init__(self, body: bytes):
        self._buf = BytesIO(body)

    def read(self):
        return self._buf.read()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_fetch_emoji_list_success():
    payload = json.dumps({"ok": True, "emoji": {"parrot": "https://x/parrot.gif"}}).encode()
    with patch("urllib.request.urlopen", return_value=_FakeResponse(payload)):
        assert fetch_emoji_list("xoxp-fake") == {"parrot": "https://x/parrot.gif"}


def test_fetch_emoji_list_api_error():
    payload = json.dumps({"ok": False, "error": "invalid_auth"}).encode()
    with patch("urllib.request.urlopen", return_value=_FakeResponse(payload)):
        try:
            fetch_emoji_list("xoxp-bad")
        except RuntimeError as error:
            assert "invalid_auth" in str(error)
        else:
            raise AssertionError("expected RuntimeError")


def test_download_emoji_writes_file(tmp_path):
    with patch("urllib.request.urlopen", return_value=_FakeResponse(b"binary-image-data")):
        target = download_emoji("parrot", "https://x/parrot.gif", tmp_path)
    assert target == tmp_path / "parrot.gif"
    assert target.read_bytes() == b"binary-image-data"


def test_open_https_rejects_non_https_schemes():
    import urllib.request

    from slack_emojis.fetch_slack_emojis import open_https

    for url in ("file:///etc/passwd", "http://example.com/x.png", "ftp://x/y.png"):
        try:
            open_https(urllib.request.Request(url))
        except ValueError as error:
            assert "refusing non-HTTPS" in str(error)
        else:
            raise AssertionError(f"expected {url} to be refused")
