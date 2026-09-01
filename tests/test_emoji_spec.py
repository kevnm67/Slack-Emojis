import pytest
from PIL import Image

from slack_emojis.emoji_spec import MAX_BYTES, validate


@pytest.fixture
def make_image(tmp_path):
    """Write a real image file and return its path."""

    def _make(name="test.png", size=(128, 128), image_format="PNG", frames=1):
        path = tmp_path / name
        image = Image.new("RGBA", size, (255, 0, 0, 255))
        if frames > 1:
            # Each frame must differ or Pillow collapses them into one.
            extra = [
                Image.new("RGBA", size, (i % 256, (i * 7) % 256, (i * 13) % 256, 255))
                for i in range(1, frames)
            ]
            image.save(path, format=image_format, save_all=True, append_images=extra)
        else:
            image.save(path, format=image_format)
        return path

    return _make


def test_valid_square_png_passes(make_image):
    report = validate(make_image())
    assert report.ok
    assert report.image_format == "PNG"
    assert report.size == (128, 128)
    assert not report.warnings


def test_non_square_is_a_warning_not_an_error(make_image):
    report = validate(make_image(size=(128, 64)))
    assert report.ok
    assert any("not square" in w for w in report.warnings)


def test_small_square_warns_about_retina(make_image):
    report = validate(make_image(size=(32, 32)))
    assert report.ok
    assert any("retina" in w for w in report.warnings)


def test_oversize_file_fails(make_image, monkeypatch):
    path = make_image()
    monkeypatch.setattr(type(path), "stat", lambda self: _FakeStat(MAX_BYTES + 1))
    report = validate(path)
    assert not report.ok
    assert any("128 KB" in e for e in report.errors)


def test_too_many_gif_frames_fails(make_image):
    report = validate(make_image("anim.gif", image_format="GIF", frames=60))
    assert not report.ok
    assert any("at most 50" in e for e in report.errors)


def test_gif_under_frame_limit_passes(make_image):
    report = validate(make_image("anim.gif", image_format="GIF", frames=10))
    assert report.ok


def test_unreadable_file_fails(tmp_path):
    path = tmp_path / "fake.png"
    path.write_bytes(b"this is definitely not a png")
    report = validate(path)
    assert not report.ok
    assert any("not a readable image" in e for e in report.errors)


def test_missing_file_fails(tmp_path):
    report = validate(tmp_path / "nope.png")
    assert not report.ok
    assert any("does not exist" in e for e in report.errors)


def test_name_is_sanitized_to_snake_case(make_image):
    report = validate(make_image(), name="HashiCorp Terraform")
    assert report.name == "hashicorp_terraform"
    assert report.ok


def test_duplicate_name_fails(make_image):
    report = validate(make_image(), name="parrot", existing={"parrot"})
    assert not report.ok
    assert any("already exists" in e for e in report.errors)


def test_svg_is_rejected(tmp_path):
    path = tmp_path / "logo.svg"
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
    report = validate(path)
    assert not report.ok


class _FakeStat:
    def __init__(self, size):
        self.st_size = size


def test_audit_finds_duplicate_names(tmp_path, monkeypatch):
    from slack_emojis import emoji_spec

    (tmp_path / "parrot.png").write_bytes(b"x")
    (tmp_path / "parrot.gif").write_bytes(b"x")
    (tmp_path / "unique.png").write_bytes(b"x")
    monkeypatch.setattr(emoji_spec, "EMOJI_DIR", tmp_path)

    reports = emoji_spec.audit_duplicate_names()
    assert len(reports) == 1
    assert reports[0].name == "parrot"
    assert not reports[0].ok


def test_audit_passes_when_names_are_unique(tmp_path, monkeypatch):
    from slack_emojis import emoji_spec

    (tmp_path / "parrot.png").write_bytes(b"x")
    (tmp_path / "unique.gif").write_bytes(b"x")
    monkeypatch.setattr(emoji_spec, "EMOJI_DIR", tmp_path)

    assert emoji_spec.audit_duplicate_names() == []


def test_copyright_flags_missing_provenance(make_image):
    report = validate(make_image(), name="totally_new_thing")
    assert report.ok  # advisory only
    assert any("no provenance" in n for n in report.copyright_notes)


def test_copyright_flags_brand_names(make_image):
    report = validate(make_image(), name="nintendo_thing")
    assert report.ok
    assert any("third-party IP" in n for n in report.copyright_notes)


def test_copyright_silent_for_recorded_provenance(make_image, monkeypatch, tmp_path):
    import json

    from slack_emojis import emoji_spec

    provenance = tmp_path / "provenance.json"
    provenance.write_text(json.dumps({"emoji": {"safe_name": {"source": "x", "license": "MIT"}}}))
    monkeypatch.setattr(emoji_spec, "PROVENANCE_FILE", provenance)

    report = emoji_spec.validate(make_image(), name="safe_name")
    assert report.copyright_notes == []
