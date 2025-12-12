# tests/test_gettext_api.py
# type: ignore

from pathlib import Path

from pypomo.gettext import _, translation


def test_gettext_and_underscore(tmp_path):
    loc = tmp_path / "ja" / "LC_MESSAGES"
    loc.mkdir(parents=True)

    po = loc / "messages.po"
    po.write_text(
        'msgid ""\n'
        'msgstr ""\n'
        '"Language: ja\\n"\n'
        '"Plural-Forms: nplurals=1; plural=0;\\n"\n'
        '\n'
        'msgid "Hello"\n'
        'msgstr "こんにちは"\n'
        '\n'
        'msgid "apple"\n'
        'msgid_plural "apples"\n'
        'msgstr[0] "りんご"\n'
    )

    translation("messages", str(tmp_path), ["ja"])

    assert _("Hello") == "こんにちは"
    assert _("apple", plural="apples", n=1) == "りんご"
    assert _("apple", plural="apples", n=5) == "りんご"
