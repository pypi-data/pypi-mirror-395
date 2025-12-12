# tests/test_po_parser.py

from pathlib import Path
from pypomo.parser.po_parser import POParser

def test_parse_simple_po(tmp_path):
    po = tmp_path / "test.po"
    po.write_text(
        'msgid ""\n'
        'msgstr ""\n'
        '"Language: ja\\n"\n'
        '"Plural-Forms: nplurals=1; plural=0;\\n"\n'
        '\n'
        'msgid "Hello"\n'
        'msgstr "こんにちは"\n'
    )

    parser = POParser()
    entries = parser.parse(po)

    # Entry count
    assert len(entries) == 2
    header, hello = entries

    assert header.msgid == ""
    assert "Language:" in header.msgstr

    assert hello.msgid == "Hello"
    assert hello.msgstr == "こんにちは"

