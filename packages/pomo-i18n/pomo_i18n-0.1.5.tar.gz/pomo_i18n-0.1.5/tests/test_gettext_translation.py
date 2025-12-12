# tests/test_gettext_translation.py
# type: ignore

from __future__ import annotations

from pathlib import Path

from pypomo.gettext import translation


def test_translation_loads_po_and_applies_plural_rules(write_po) -> None:
    lines = [
        'msgid ""',
        'msgstr ""',
        '"Language: en\\n"',
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"',
        "",
        'msgid "Hello"',
        'msgstr "Hello!"',
        "",
        'msgid "apple"',
        'msgid_plural "apples"',
        'msgstr[0] "apple"',
        'msgstr[1] "apples"',
    ]

    # create locales/en/LC_MESSAGES/messages.po
    po_path: Path = write_po("messages", "en", lines)

    # localedir = .../locales
    localedir = str(po_path.parent.parent.parent)

    catalog = translation(
        domain="messages", localedir=localedir, languages=["en"]
    )

    assert catalog.gettext("Hello") == "Hello!"
    assert catalog.ngettext("apple", "apples", 1) == "apple"
    assert catalog.ngettext("apple", "apples", 3) == "apples"
