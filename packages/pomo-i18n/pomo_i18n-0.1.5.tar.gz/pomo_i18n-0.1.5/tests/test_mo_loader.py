# tests/test_mo_loader.py
# type: ignore

import gettext
from pathlib import Path

from pypomo.catalog import Catalog
from pypomo.mo.loader import load_mo
from pypomo.mo.writer import write_mo
from pypomo.parser.types import POEntry


# ---------------------------------------------------
# 1. Basic single-message round-trip
# ---------------------------------------------------
def test_load_mo_basic(tmp_path):
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: en\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=2; plural=(n != 1);\n"
            ),
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry("Hello", "Hello!!", None, {}, []),
    ]

    po_cat = Catalog.from_po_entries(entries)

    mo_path = tmp_path / "basic.mo"
    write_mo(mo_path, po_cat)

    # Load back as Catalog
    cat = load_mo(mo_path)

    assert cat.gettext("Hello") == "Hello!!"
    assert cat.plural_rule is not None
    assert cat.plural_rule(1) == 0
    assert cat.plural_rule(2) == 1


# ---------------------------------------------------
# 2. plural forms round-trip
# ---------------------------------------------------
def test_load_mo_plural(tmp_path):
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: en\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=2; plural=(n != 1);\n"
            ),
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

    cat0 = Catalog.from_po_entries(entries)

    mo_path = tmp_path / "plural.mo"
    write_mo(mo_path, cat0)

    cat = load_mo(mo_path)

    assert cat.ngettext("apple", "apples", 1) == "apple"
    assert cat.ngettext("apple", "apples", 5) == "apples"


# ---------------------------------------------------
# 3. plural missing → fallback auto-fill
# ---------------------------------------------------
def test_load_mo_plural_missing_forms(tmp_path):
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
            msgstr_plural={0: "ボール"},
            comments=[],
        ),
    ]

    po_cat = Catalog.from_po_entries(entries)
    mo_path = tmp_path / "missing.mo"
    write_mo(mo_path, po_cat)

    cat = load_mo(mo_path)

    assert cat.ngettext("ball", "ボールたち", 1) == "ボール"
    assert cat.ngettext("ball", "ボールたち", 2) == "ボールたち"
    assert cat.ngettext("ball", "ボールたち", 5) == "ボールたち"


# ---------------------------------------------------
# 4. header is correctly read and applied
# ---------------------------------------------------
def test_load_mo_header(tmp_path):
    entries = [
        POEntry(
            msgid="",
            msgstr=(
                "Language: fr\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Plural-Forms: nplurals=2; plural=(n > 1);\n"
            ),
            msgid_plural=None,
            msgstr_plural={},
            comments=[],
        ),
        POEntry("cat", "chat", None, {}, []),
    ]

    po_cat = Catalog.from_po_entries(entries)
    mo_path = tmp_path / "header.mo"
    write_mo(mo_path, po_cat)

    cat = load_mo(mo_path)

    assert cat.plural_rule is not None
    # French rule: n > 1 → plural index 1
    assert cat.plural_rule(1) == 0
    assert cat.plural_rule(2) == 1

    assert cat.gettext("cat") == "chat"
