# tests/test_mo_writer.py
# type: ignore

import gettext
from pathlib import Path

from pypomo.catalog import Catalog
from pypomo.mo.writer import write_mo
from pypomo.parser.types import POEntry


# ---------------------------------------------------
# 1. Header present (basic functionality)
# ---------------------------------------------------
def test_mo_writer_basic(tmp_path):
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: ja\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=1; plural=0;\n"
            ),
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

    cat = Catalog.from_po_entries(entries)
    mo_file = tmp_path / "basic.mo"
    write_mo(mo_file, cat)

    trans = gettext.GNUTranslations(open(mo_file, "rb"))
    assert trans.gettext("Hello") == "こんにちは"


# ---------------------------------------------------
# 2. Header missing → fallback header generation
# ---------------------------------------------------
def test_mo_writer_fallback_header(tmp_path):
    # No header entry (msgid="")
    entries = [
        POEntry(
            msgid="Hello",
            msgstr="Hello!",
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        )
    ]

    cat = Catalog.from_po_entries(entries)
    mo_file = tmp_path / "fallback.mo"
    write_mo(mo_file, cat)

    trans = gettext.GNUTranslations(open(mo_file, "rb"))

    # Should still translate
    assert trans.gettext("Hello") == "Hello!"

    # Fallback header must contain at least Plural-Forms
    hdr = trans._info
    assert "plural-forms" in hdr


# ---------------------------------------------------
# 3. plural=2 with full plural forms
# ---------------------------------------------------
def test_mo_writer_plural_two_forms(tmp_path):
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: ja\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=2; plural=(n != 1);\n"
            ),
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry(
            msgid="apple",
            msgstr="りんご",
            msgid_plural="りんごたち",
            msgstr_plural={0: "りんご", 1: "りんごたち"},
            comments=[],
        ),
    ]

    cat = Catalog.from_po_entries(entries)
    mo_file = tmp_path / "plural2.mo"
    write_mo(mo_file, cat)

    trans = gettext.GNUTranslations(open(mo_file, "rb"))
    assert trans.ngettext("apple", "りんごたち", 1) == "りんご"
    assert trans.ngettext("apple", "りんごたち", 5) == "りんごたち"


# ---------------------------------------------------
# 4. plural missing entries → mo_writer should auto-fill
# ---------------------------------------------------
def test_mo_writer_plural_missing_forms(tmp_path):
    # nplurals=3 but only form0 is present
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: ja\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=3; plural=(n != 1);\n"
            ),
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry(
            msgid="ball",
            msgstr="ボール",
            msgid_plural="ボールたち",
            msgstr_plural={0: "ボール"},  # only form0
            comments=[],
        ),
    ]

    cat = Catalog.from_po_entries(entries)
    mo_file = tmp_path / "plural_missing.mo"
    write_mo(mo_file, cat)

    trans = gettext.GNUTranslations(open(mo_file, "rb"))

    # form0 = ボール
    # form1, form2 = fallback → plural string
    assert trans.ngettext("ball", "ボールたち", 1) == "ボール"
    assert trans.ngettext("ball", "ボールたち", 2) == "ボールたち"
    assert trans.ngettext("ball", "ボールたち", 5) == "ボールたち"


# ---------------------------------------------------
# 5. msgid sorted order
# ---------------------------------------------------
def test_mo_writer_sorted_order(tmp_path):
    entries = [
        POEntry("", "Plural-Forms: nplurals=1; plural=0;\n", None, {}, []),
        POEntry("banana", "バナナ", None, {}, []),
        POEntry("apple", "りんご", None, {}, []),
    ]

    cat = Catalog.from_po_entries(entries)
    mo_file = tmp_path / "sorted.mo"
    write_mo(mo_file, cat)

    data = mo_file.read_bytes()

    # msgids should appear in order: "" < "apple" < "banana"
    assert data.find(b"apple") < data.find(b"banana")


# ---------------------------------------------------
# 6. Write and read
# ---------------------------------------------------
def test_write_and_read_mo(tmp_path):
    # ----- Build catalog -----
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: ja\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=1; plural=0;\n"
            ),
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
        POEntry(
            msgid="apple",
            msgstr="りんご",
            msgid_plural="apples",
            msgstr_plural={0: "りんご"},
            comments=[],
        ),
    ]

    cat = Catalog.from_po_entries(entries)

    mo_path = tmp_path / "messages.mo"
    write_mo(mo_path, cat)

    # ----- Read using Python's builtin gettext -----
    # trans = gettext.GNUTranslations(open(mo_path, "rb"))

    with mo_path.open("rb") as f:
        trans = gettext.GNUTranslations(f)

    assert trans.gettext("Hello") == "こんにちは"
    assert trans.ngettext("apple", "apples", 1) == "りんご"
    assert trans.ngettext("apple", "apples", 5) == "りんご"
