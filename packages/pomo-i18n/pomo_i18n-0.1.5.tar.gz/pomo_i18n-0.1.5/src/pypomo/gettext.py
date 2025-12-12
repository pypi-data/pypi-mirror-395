# src/pypomo/gettext.py

from __future__ import annotations

from pathlib import Path

from .catalog import Catalog
from .parser.po_parser import POParser

# ----------------------------------------
# Default catalog (always updated by translation())
# ----------------------------------------
_default_catalog: Catalog | None = None


def get_default_catalog() -> Catalog:
    """
    Always return the latest catalog.
    If not initialized, return an empty one.

    This avoids Python import-time binding problems.
    """
    global _default_catalog
    if _default_catalog is None:
        _default_catalog = Catalog()
    return _default_catalog


# ----------------------------------------
# Public gettext APIs
# ----------------------------------------
def gettext(msgid: str) -> str:
    """
    Translate msgid using the default catalog.
    """
    catalog = get_default_catalog()
    return catalog.gettext(msgid)


def ngettext(singular: str, plural: str, n: int) -> str:
    """
    Plural-aware translate using the default catalog.
    """
    catalog = get_default_catalog()
    return catalog.ngettext(singular, plural, n)


def _(msgid: str, *, plural: str | None = None, n: int | None = None) -> str:
    """
    Shortcut gettext function like GNU gettext.

    Usage:
        _("Hello")
        _("apple", plural="apples", n=3)
        _("apple", n=3)  # plural autodetected as "apples"
    """
    catalog = get_default_catalog()

    if n is None:
        return catalog.gettext(msgid)

    if plural is None:
        plural = msgid + "s"  # fallback plural

    return catalog.ngettext(msgid, plural, n)


# ----------------------------------------
# translation() - like gettext.translation()
# Loads PO files and sets the global catalog.
# ----------------------------------------
def translation(
    domain: str,
    localedir: str,
    languages: list[str] | None = None,
) -> Catalog:
    """
    Load translations from .po files for the selected domain/languages.

    This is a strict/mypy-friendly implementation.
    """
    global _default_catalog

    langs = languages or []
    parser = POParser()

    catalog = Catalog(
        domain=domain,
        localedir=localedir,
        languages=langs,
    )

    for lang in langs:
        po_path = Path(localedir) / lang / "LC_MESSAGES" / f"{domain}.po"

        if not po_path.exists():
            continue

        entries = parser.parse(po_path)
        part = Catalog.from_po_entries(entries)

        # Merge into main catalog
        catalog.merge(part)

    # update global catalog
    _default_catalog = catalog

    return catalog
