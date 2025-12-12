# src/pypomo/catalog.py

from __future__ import annotations

from collections.abc import ValuesView
from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from pypomo.parser.types import POEntry
from pypomo.utils.plural_forms import PluralRule


@dataclass(slots=True)
class CatalogMessage:
    """Represents a single resolved message in a catalog."""

    msgid: str
    singular: str
    plural: str | None = None
    translations: Dict[int, str] = field(
        default_factory=lambda: dict[int, str]()
    )


class Catalog:
    """
    In-memory message catalog.

    Responsibilities:
        - Provide gettext / ngettext translation lookups
        - Manage plural rules via Plural-Forms
        - Build message objects from POEntry structures

    Internal notice:
        - __messages is considered private
        - External code should not rely on its structure

    """

    def __init__(
        self,
        domain: str | None = None,
        localedir: str | None = None,
        languages: Iterable[str] | None = None,
    ) -> None:
        self.domain = domain
        self.localedir = localedir
        self.languages = list(languages) if languages is not None else None

        # Private internal storage of messages
        self.__messages: Dict[str, CatalogMessage] = {}

        # Plural forms evaluator (None until loaded from header)
        self.plural_rule: PluralRule | None = None
        # Keep nplurals for compatibility with tests / mo_writer
        self.nplurals: int | None = None

        # header
        self._header_raw: str = ""

    # ----------------------------------------
    # Private getters for internal state (Step 2 additions)
    # ----------------------------------------
    def _iter_messages(self) -> ValuesView[CatalogMessage]:
        """Internal-only: iterate over stored Message objects."""
        return self.__messages.values()

    # ----------------------------------------
    # Header: Parse plural-forms
    # ----------------------------------------
    def _load_header(self, header_msgstr: str) -> None:
        """
        Try to extract a Plural-Forms rule from the header msgstr.

        The header is a concatenated string of lines like:
            "Language: en\\n"
            "Plural-Forms: nplurals=2; plural=(n != 1);\\n"
        """
        if "Plural-Forms" not in header_msgstr:
            return

        try:
            rule = PluralRule.from_header(header_msgstr)
            self.plural_rule = rule
            self.nplurals = rule.nplurals
        except Exception:
            # Fail-safe: leave plural_rule / nplurals as-is
            pass

    # ----------------------------------------
    # Lookup API
    # ----------------------------------------
    def gettext(self, msgid: str) -> str:
        """Return translated string or msgid if not found."""
        message = self.__messages.get(msgid)
        if message is None:
            return msgid

        # No plural translations -> use singular
        if not message.translations:
            return message.singular

        # Singular form = index 0
        return message.translations.get(0, message.singular)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        """
        Return plural-aware translation.

        If plural_rule is available, its result is used as plural index.
        Otherwise falls back to an English-like rule: 0 if n == 1 else 1.
        """
        message = self.__messages.get(singular)

        if message is None:
            # No translation → return original strings
            return singular if n == 1 else plural

        # select index
        if self.plural_rule is None:
            # Fallback: English-style behavior
            index = 0 if n == 1 else 1
        else:
            index = self.plural_rule(n)

        # Use translated plural form if available
        if index in message.translations:
            return message.translations[index]

        # Missing plural entry -> conservative fallback
        if index == 0:
            return message.singular
        return message.plural or plural

    # ----------------------------------------
    # Mutation helpers
    # ----------------------------------------
    def add_message(self, message: CatalogMessage) -> None:
        """Add or replace a single message."""
        self.__messages[message.msgid] = message

    def merge(self, other: Catalog) -> None:
        """
        Merge messages from another Catalog.

        This is a public helper that keeps __messages private, while still
        allowing catalogs built from different PO files to be merged.
        """
        # Accessing __messages is allowed from within the same class
        self.__messages.update(other.__messages)

        # If the current catalog has no plural_rule yet, inherit from other
        if self.plural_rule is None and other.plural_rule is not None:
            self.plural_rule = other.plural_rule
            self.nplurals = other.nplurals

    # ----------------------------------------
    # Construction helpers
    # ----------------------------------------
    @classmethod
    def from_po_entries(cls, entries: List[POEntry]) -> Catalog:
        """
        Build a Catalog from a list of POEntry objects.

        This will:
            - Extract Plural-Forms from the header entry (msgid == "")
            - Convert all non-header entries into Message instances
        """
        catalog = cls()

        # messages
        for entry in entries:

            # header
            if entry.msgid == "":
                catalog._header_raw = entry.msgstr
                catalog._load_header(entry.msgstr)
                continue

            # normal entry
            # singular msgstr or fallback to msgid
            singular = entry.msgstr if entry.msgstr else entry.msgid

            msg = CatalogMessage(
                msgid=entry.msgid,
                singular=singular,
                plural=entry.msgid_plural,
                translations=entry.msgstr_plural.copy(),
            )

            catalog.add_message(msg)

        return catalog

    def header_msgstr(self) -> str:
        return self._header_raw or ""

    def add_singular(self, msgid: str, msgstr: str) -> None:
        # Fallback: empty msgstr → use msgid
        singular = msgstr if msgstr else msgid

        self.__messages[msgid] = CatalogMessage(
            msgid=msgid,
            singular=singular,
            plural=None,
            translations={},
        )

        # If Header (msgid == ""), also update _header_raw
        if msgid == "":
            self._header_raw = singular
            # If no plural_rule yet, interpret it here
            if self.plural_rule is None:
                self._load_header(singular)

    def add_plural(
        self,
        msgid: str,
        msgid_plural: str,
        forms: list[str],
    ) -> None:
        # If form[0] exists, it will be used as singular,
        # otherwise msgid will be used as fallback.
        singular: str = ""
        if forms:
            singular = forms[0]
        else:
            singular = msgid

        plural_map: Dict[int, str] = {i: f for i, f in enumerate(forms)}

        self.__messages[msgid] = CatalogMessage(
            msgid=msgid,
            singular=singular,
            plural=msgid_plural,
            translations=plural_map,
        )
