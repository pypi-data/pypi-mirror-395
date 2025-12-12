# src/pypomo/mo/catalog_builder.py

from __future__ import annotations

from typing import Dict, Iterable

from pypomo.catalog import Catalog
from pypomo.utils.plural_forms import PluralRule

from .types import DecodedItem


def build_catalog_from_pairs(
    pairs: Iterable[DecodedItem],
    header_info: Dict[str, str],
) -> Catalog:
    """
    Build a Catalog from decoded (msgid, msgstr) pairs.

    plural entries come as:
        ("plural-header", (singular, plural, forms))

    single entries:
        ("single", (msgid, msgstr))

    Returns a populated Catalog instance.
    """
    catalog = Catalog()

    # Header (Plural-Forms)
    plural_form_line = header_info.get("plural-forms")
    if plural_form_line:
        catalog.plural_rule = PluralRule.from_header(plural_form_line)

    # Messages
    for item in pairs:
        if item["kind"] == "single":
            msgid: str = item["msgid"]
            msgstr: str = item["msgstr"]

            if msgid == "":
                # header -> already handled
                continue

            catalog.add_singular(msgid, msgstr)

        elif item["kind"] == "plural-header":
            singular = item["singular"]
            plural = item["plural"]
            forms = item["forms"]

            catalog.add_plural(singular, plural, forms)

    return catalog
