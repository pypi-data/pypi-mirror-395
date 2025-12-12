# tests/test_plural_forms.py
# type: ignore

from pypomo.catalog import Catalog
from pypomo.parser.types import POEntry


# ------------------------------------
# Japanese: nplurals=1; plural=0;
# ------------------------------------
def test_plural_forms_japanese():
    entries = [
        POEntry(
            msgid="",
            msgstr="Language: ja\nPlural-Forms: nplurals=1; plural=0;\n",
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry(
            msgid="apple",
            msgstr="りんご",
            msgid_plural="apples",
            msgstr_plural={0: "りんご"},
            comments=[],
        ),
    ]

    cat = Catalog.from_po_entries(entries)

    assert cat.ngettext("apple", "apples", 1) == "りんご"
    assert cat.ngettext("apple", "apples", 5) == "りんご"


# ------------------------------------
# English: nplurals=2; plural=(n != 1);
# ------------------------------------
def test_plural_forms_english():
    entries = [
        POEntry(
            msgid="",
            msgstr="Language: en\nPlural-Forms: nplurals=2; plural=(n != 1);\n",
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry(
            msgid="apple",
            msgstr="apple",
            msgid_plural="apples",
            msgstr_plural={0: "apple", 1: "apples"},
            comments=[],
        ),
    ]

    cat = Catalog.from_po_entries(entries)

    assert cat.ngettext("apple", "apples", 1) == "apple"
    assert cat.ngettext("apple", "apples", 5) == "apples"
