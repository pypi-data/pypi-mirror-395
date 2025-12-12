# tests/test_catalog_plural.py
# type: ignore

from __future__ import annotations

from pypomo.catalog import Catalog
from pypomo.parser.types import POEntry


def test_catalog_from_po_entries_plural_forms_english() -> None:
    # Header entry (msgid == "")
    header = POEntry(
        msgid="",
        msgstr=(
            "Language: en\n" "Plural-Forms: nplurals=2; plural=(n != 1);\n"
        ),
    )

    # Normal pluralized entry
    entry = POEntry(
        msgid="apple",
        msgstr="",
        msgid_plural="apples",
        msgstr_plural={0: "apple", 1: "apples"},
    )

    catalog = Catalog.from_po_entries([header, entry])

    # nplurals should be 2 for English
    assert catalog.nplurals == 2

    # plural rules: n != 1
    assert catalog.ngettext("apple", "apples", 1) == "apple"
    assert catalog.ngettext("apple", "apples", 2) == "apples"
    assert catalog.ngettext("apple", "apples", 10) == "apples"


def test_catalog_from_po_entries_plural_forms_japanese() -> None:
    # Japanese: nplurals=1; plural=0; (always singular)
    header = POEntry(
        msgid="",
        msgstr=("Language: ja\n" "Plural-Forms: nplurals=1; plural=0;\n"),
    )

    entry = POEntry(
        msgid="apple",
        msgstr="りんご",
        msgid_plural=None,
        msgstr_plural={},
    )

    catalog = Catalog.from_po_entries([header, entry])

    # Japanese uses single plural index
    assert catalog.nplurals == 1

    # Any n should return singular
    assert catalog.ngettext("apple", "apples", 1) == "りんご"
    assert catalog.ngettext("apple", "apples", 3) == "りんご"
