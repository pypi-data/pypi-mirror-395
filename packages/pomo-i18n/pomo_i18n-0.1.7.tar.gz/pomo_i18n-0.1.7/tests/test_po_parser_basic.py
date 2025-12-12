# tests/test_po_parser_basic.py
# type: ignore

from __future__ import annotations

from pathlib import Path

from pypomo.parser.po_parser import POParser
from pypomo.parser.types import POEntry


def test_po_parser_parses_singular_and_plural(tmp_path: Path) -> None:
    po_content = [
        'msgid ""',
        'msgstr ""',
        '"Language: en\\n"',
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"',
        "",
        'msgid "apple"',
        'msgid_plural "apples"',
        'msgstr[0] "apple"',
        'msgstr[1] "apples"',
    ]

    po_path = tmp_path / "test.po"
    po_path.write_text("\n".join(po_content), encoding="utf-8")

    parser = POParser()
    entries = parser.parse(po_path)

    # header + 1 entry
    assert len(entries) == 2

    header = entries[0]
    assert isinstance(header, POEntry)
    assert header.msgid == ""
    assert "Plural-Forms" in header.msgstr

    entry = entries[1]
    assert entry.msgid == "apple"
    assert entry.msgid_plural == "apples"
    assert entry.msgstr_plural[0] == "apple"
    assert entry.msgstr_plural[1] == "apples"
