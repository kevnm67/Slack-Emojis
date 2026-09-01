"""Exercise the command-line entry points end to end."""

import json

import pytest
from PIL import Image

from slack_emojis import emoji_spec, update_emojis


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A miniature repo: Emojis/, a README with the generated markers, provenance."""
    emoji_dir = tmp_path / "Emojis"
    emoji_dir.mkdir()
    Image.new("RGBA", (128, 128), (255, 0, 0, 255)).save(emoji_dir / "parrot.png")
    Image.new("RGBA", (128, 128), (0, 255, 0, 255)).save(emoji_dir / "Shouty Name.png")

    readme = tmp_path / "README.md"
    readme.write_text("# Title\n\n## Emojis\n\nold table\n\n## Attribution\n\ncredits\n")

    provenance = tmp_path / "provenance.json"
    provenance.write_text(json.dumps({"emoji": {"parrot": {"source": "x", "license": "MIT"}}}))

    monkeypatch.setattr(update_emojis, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(emoji_spec, "EMOJI_DIR", emoji_dir)
    monkeypatch.setattr(emoji_spec, "PROVENANCE_FILE", provenance)
    return tmp_path


def test_update_emojis_rewrites_the_table(repo, monkeypatch):
    monkeypatch.setattr("sys.argv", ["update_emojis"])
    assert update_emojis.main() == 0

    readme = (repo / "README.md").read_text()
    assert "| parrot |" in readme
    assert "old table" not in readme
    assert readme.startswith("# Title")
    assert "## Attribution" in readme


def test_update_emojis_dry_run_leaves_readme_alone(repo, monkeypatch, capsys):
    before = (repo / "README.md").read_text()
    monkeypatch.setattr("sys.argv", ["update_emojis", "--dry-run"])

    assert update_emojis.main() == 0
    assert (repo / "README.md").read_text() == before
    assert "| parrot |" in capsys.readouterr().out


def test_update_emojis_sanitizes_filenames_on_disk(repo, monkeypatch):
    monkeypatch.setattr("sys.argv", ["update_emojis"])
    update_emojis.main()

    names = {p.name for p in (repo / "Emojis").iterdir()}
    assert "shouty_name.png" in names
    assert "Shouty Name.png" not in names


def test_validate_cli_passes_a_good_file(repo, monkeypatch, capsys):
    good = repo / "candidate.png"
    Image.new("RGBA", (128, 128), (0, 0, 255, 255)).save(good)
    monkeypatch.setattr("sys.argv", ["emoji_spec", str(good), "--name", "brand_new"])

    assert emoji_spec.main() == 0
    assert "PASS" in capsys.readouterr().out


def test_validate_cli_fails_a_duplicate(repo, monkeypatch, capsys):
    dupe = repo / "candidate.png"
    Image.new("RGBA", (128, 128), (0, 0, 255, 255)).save(dupe)
    monkeypatch.setattr("sys.argv", ["emoji_spec", str(dupe), "--name", "parrot"])

    assert emoji_spec.main() == 1
    assert "already exists" in capsys.readouterr().out


def test_validate_cli_json_output_is_parseable(repo, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["emoji_spec", str(repo / "Emojis" / "parrot.png"), "--json"])
    emoji_spec.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["name"] == "parrot"
    assert "ok" in payload[0]


def test_audit_cli_checks_the_whole_collection(repo, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["emoji_spec", "--audit"])
    emoji_spec.main()
    assert "passed" in capsys.readouterr().out


def test_committing_flag_blocks_on_missing_provenance(repo, monkeypatch):
    candidate = repo / "candidate.png"
    Image.new("RGBA", (128, 128), (0, 0, 255, 255)).save(candidate)
    monkeypatch.setattr("sys.argv", ["emoji_spec", str(candidate), "--committing"])

    assert emoji_spec.main() == 1


def test_strict_flag_turns_warnings_into_failures(repo, monkeypatch):
    small = repo / "small.png"
    Image.new("RGBA", (32, 32), (0, 0, 255, 255)).save(small)
    monkeypatch.setattr("sys.argv", ["emoji_spec", str(small), "--name", "tiny", "--strict"])

    assert emoji_spec.main() == 1


def test_cli_requires_a_path_or_audit(monkeypatch):
    monkeypatch.setattr("sys.argv", ["emoji_spec"])
    with pytest.raises(SystemExit):
        emoji_spec.main()


def test_cli_rejects_name_with_multiple_paths(repo, monkeypatch):
    monkeypatch.setattr("sys.argv", ["emoji_spec", "a.png", "b.png", "--name", "x"])
    with pytest.raises(SystemExit):
        emoji_spec.main()


def test_fetch_cli_downloads_and_regenerates(repo, monkeypatch, capsys):
    """Drive fetch_slack_emojis.main() with the network faked out."""
    import json as _json
    from io import BytesIO

    from slack_emojis import fetch_slack_emojis

    monkeypatch.setattr(fetch_slack_emojis, "REPO_ROOT", repo)

    payload = _json.dumps(
        {
            "ok": True,
            "emoji": {
                "newbird": "https://x/newbird.png",
                "alias_bird": "alias:newbird",
            },
        }
    ).encode()
    image_bytes = (repo / "Emojis" / "parrot.png").read_bytes()

    class _Resp:
        def __init__(self, body):
            self._buf = BytesIO(body)

        def read(self):
            return self._buf.read()

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    calls = {"n": 0}

    def fake_open(request):
        calls["n"] += 1
        return _Resp(payload if "emoji.list" in request.full_url else image_bytes)

    monkeypatch.setattr(fetch_slack_emojis, "open_https", fake_open)
    monkeypatch.setattr(
        "sys.argv",
        [
            "fetch",
            "--token",
            "xoxp-fake",
            "--dest",
            str(repo / "Emojis"),
            "--delay",
            "0",
        ],
    )

    assert fetch_slack_emojis.main() == 0
    assert (repo / "Emojis" / "newbird.png").exists()
    assert (repo / "Emojis" / "alias_bird.png").exists()  # alias resolved to a real image
    assert "downloaded" in capsys.readouterr().out


def test_fetch_cli_dry_run_writes_nothing(repo, monkeypatch, capsys):
    import json as _json
    from io import BytesIO

    from slack_emojis import fetch_slack_emojis

    monkeypatch.setattr(fetch_slack_emojis, "REPO_ROOT", repo)
    payload = _json.dumps({"ok": True, "emoji": {"ghost": "https://x/ghost.png"}}).encode()

    class _Resp:
        def __init__(self, body):
            self._buf = BytesIO(body)

        def read(self):
            return self._buf.read()

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(fetch_slack_emojis, "open_https", lambda r: _Resp(payload))
    monkeypatch.setattr(
        "sys.argv",
        ["fetch", "--token", "xoxp-fake", "--dest", str(repo / "Emojis"), "--dry-run"],
    )

    assert fetch_slack_emojis.main() == 0
    assert not (repo / "Emojis" / "ghost.png").exists()
    assert "would download" in capsys.readouterr().out


def test_fetch_cli_errors_without_a_token(monkeypatch):
    from slack_emojis import fetch_slack_emojis

    monkeypatch.delenv("SLACK_TOKEN", raising=False)
    monkeypatch.setattr("sys.argv", ["fetch"])
    with pytest.raises(SystemExit):
        fetch_slack_emojis.main()
