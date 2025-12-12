# src/pypomo/__init__.py

"""
pomo-i18n: small gettext-compatible i18n helper.

Public API:

    - gettext(msgid: str) -> str
    - ngettext(singular: str, plural: str, n: int) -> str
    - _(msgid: str, *, plural: str | None = None, n: int | None = None) -> str
    - translation(domain: str, localedir: str, languages: list[str] | None = None) -> Catalog

Advanced API:

    - Catalog: in-memory translation catalog
    - write_mo(path: str | Path, catalog: Catalog) -> None
"""

from .catalog import Catalog
from .gettext import _, get_default_catalog, gettext, ngettext, translation

__all__ = [
    # gettext-style API
    "gettext",
    "ngettext",
    "_",
    "translation",
    "get_default_catalog",
    # advanced / power-user API
    "Catalog",
]
