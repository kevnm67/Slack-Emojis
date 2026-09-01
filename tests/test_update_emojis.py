from slack_emojis.update_emojis import sanitize_name


def test_sanitize_name_lowercases_and_replaces_spaces():
    assert sanitize_name("HashiCorp Terraform") == "hashicorp_terraform"


def test_sanitize_name_replaces_hyphens():
    assert sanitize_name("old-man-yells") == "old_man_yells"


def test_sanitize_name_strips_invalid_chars():
    assert sanitize_name("weird!!name??") == "weirdname"


def test_sanitize_name_collapses_repeated_underscores():
    assert sanitize_name("a___b") == "a_b"


def test_sanitize_name_strips_leading_trailing_underscores():
    assert sanitize_name("_leading_trailing_") == "leading_trailing"


def test_sanitize_name_already_clean_is_unchanged():
    assert sanitize_name("already_clean") == "already_clean"
