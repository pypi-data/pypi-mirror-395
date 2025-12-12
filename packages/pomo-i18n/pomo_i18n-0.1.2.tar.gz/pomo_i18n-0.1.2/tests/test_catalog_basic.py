# tests/test_catalog_basic.py
# type: ignore

from pypomo.catalog import Catalog
from pypomo.parser.types import POEntry


def test_catalog_gettext():
    entries = [
        POEntry(
            msgid="",
            msgstr="Language: ja\nPlural-Forms: nplurals=1; plural=0;\n",
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry(
            msgid="Hello",
            msgstr="こんにちは",
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
    ]

    catalog = Catalog.from_po_entries(entries)

    assert catalog.gettext("Hello") == "こんにちは"
    assert catalog.gettext("Unknown") == "Unknown"
