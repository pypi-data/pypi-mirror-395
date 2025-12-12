# src/pypomo/mo/loader.py

from __future__ import annotations

from pathlib import Path

from pypomo.catalog import Catalog

from .binary_reader import read_mo_binary
from .catalog_builder import build_catalog_from_pairs
from .decoder import decode_map_pairs


def load_mo(path: str | Path) -> Catalog:
    """
    Load a GNU gettext `.mo` file and return a fully constructed Catalog.

    Steps:
        1. Read raw binary data from the .mo file.
        2. Parse offsets to extract msgid/msgstr tables.
        3. Decode msgid/msgstr byte strings into text.
        4. Convert plural and singular forms into structured pairs.
        5. Build a Catalog object with plural rules / header.
    """
    # Normalize path
    p = Path(path)

    # Step 1: Read the binary file → raw id/str byte arrays
    header_info, ids, strs = read_mo_binary(p)

    # Step 2: Decode msgid/msgstr pairs
    # This yields tuples like:
    #   ("single", {"msgid": "...", "msgstr": "..."})
    #   ("plural-header", {"singular": "...", "plural": "...", "forms": [...]})
    pairs = decode_map_pairs(ids, strs)

    # Step 3: Build a Catalog (handles header + plural forms + entries)
    catalog = build_catalog_from_pairs(pairs, header_info)

    return catalog
