# tests/test_catalog_merge_basic.py
# type: ignore

from pypomo.catalog import Catalog
from pypomo.parser.types import POEntry
from pypomo.utils.plural_forms import PluralRule


def test_catalog_merge_basic() -> None:
    # Catalog A
    entry_a = POEntry(
        msgid="hello",
        msgstr="Hello",
        msgid_plural=None,
        msgstr_plural={},
    )

    catA = Catalog.from_po_entries([entry_a])

    # Catalog B
    entry_b = POEntry(
        msgid="bye",
        msgstr="Goodbye",
        msgid_plural=None,
        msgstr_plural={},
    )

    catB = Catalog.from_po_entries([entry_b])

    # Merge B → A
    catA.merge(catB)

    # both messages should be present
    assert catA.gettext("hello") == "Hello"
    assert catA.gettext("bye") == "Goodbye"


def test_catalog_merge_plural_rule_inherit() -> None:
    # Catalog A (no plural rule)
    catA = Catalog()

    # Catalog B with plural rule
    header = POEntry(
        msgid="",
        msgstr="Language: en\nPlural-Forms: nplurals=2; plural=(n != 1);\n",
    )

    catB = Catalog.from_po_entries([header])

    catA.merge(catB)

    # plural rule should now be inherited
    assert catA.plural_rule is not None
    assert catA.nplurals == 2
