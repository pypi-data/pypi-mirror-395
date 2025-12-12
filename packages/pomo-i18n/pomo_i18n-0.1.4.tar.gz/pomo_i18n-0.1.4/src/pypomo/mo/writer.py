# src/pypomo/mo_writer.py

from __future__ import annotations

import struct
from pathlib import Path
from typing import Dict, List, Tuple

from pypomo.catalog import Catalog


def _build_message_map(catalog: Catalog) -> Dict[str, str]:
    """
    Build a mapping of msgid -> msgstr in the GNU MO format.

    Rules:
        - For single messages:
            msgid -> msgstr
        - For plural messages:
            msgid  = "singular\\x00plural"
            msgstr = "form0\\x00form1\\x00...\\x00formN"
    """
    result: Dict[str, str] = {}

    # ----------------------------------------
    # Header entry ("") must contain metadata
    # ----------------------------------------
    # Use catalog.header_msgstr() if available (raw PO header)
    # Otherwise build a minimal fallback header.
    header_lines: List[str] = []

    header: str = catalog.header_msgstr()  # always a str
    if not header:
        # No header found — create a minimal valid gettext header
        header_lines = [
            "Project-Id-Version: PACKAGE VERSION",
            "Report-Msgid-Bugs-To: ",
            "POT-Creation-Date: ",
            "PO-Revision-Date: ",
            "Last-Translator: ",
            "Language-Team: ",
            "MIME-Version: 1.0",
            "Content-Type: text/plain; charset=UTF-8",
            "Content-Transfer-Encoding: 8bit",
        ]

        # Language (if known)
        if catalog.languages:
            header_lines.append(f"Language: {catalog.languages[0]}")

        # Plural-Forms fallback
        npl = catalog.nplurals if catalog.nplurals is not None else 2
        if npl == 1:
            plural_expr = "0"
        elif npl == 2:
            plural_expr = "(n != 1)"
        else:
            # fallback for languages with 3+ plural forms
            plural_expr = "(n != 1)"  # safe-ish default

        header_lines.append(
            f"Plural-Forms: nplurals={npl}; plural={plural_expr};"
        )

        header = "\n".join(header_lines)

    result[""] = header

    # ----------------------------------------
    # Normal messages
    # ----------------------------------------
    for msg in catalog._iter_messages():

        # Skip header entry (msgid="")
        if msg.msgid == "":
            continue

        # No plural -> simple key/value
        if msg.plural is None or not msg.translations:
            msgid = msg.msgid
            msgstr = msg.translations.get(0, msg.singular)
            result[msgid] = msgstr
            continue

        # Plural message
        singular = msg.msgid
        plural = msg.plural or ""

        # msgid = "singular\x00plural"
        msgid = singular + "\x00" + plural

        # msgstr = join forms 0..nplurals-1
        nplurals: int = catalog.nplurals if catalog.nplurals is not None else 1

        forms: List[str] = []
        for idx in range(nplurals):
            if idx in msg.translations:
                forms.append(msg.translations[idx])
            else:
                # Fallback if the PO file didn't define enough plural forms
                if idx == 0:
                    forms.append(msg.singular)
                else:
                    forms.append(msg.plural or msg.singular)

        msgstr = "\x00".join(forms)
        result[msgid] = msgstr

    return result


def write_mo(path: str | Path, catalog: Catalog) -> None:
    """
    Write a GNU gettext-compatible .mo file from a Catalog instance.

    Format notes:
        - Little-endian (magic number 0x950412de)
        - No hash table (hash_size=0, hash_offset=0)
        - String tables store (length, absolute_offset) pairs
        - Strings are UTF-8 encoded and null-terminated
    """
    path = Path(path)

    # Build {msgid: msgstr}
    messages = _build_message_map(catalog)

    # MO spec requires msgid-sorted order
    items: List[Tuple[str, str]] = sorted(
        messages.items(), key=lambda kv: kv[0]
    )

    # Header fields
    magic = 0x950412DE  # Little-endian magic
    revision = 0
    nstrings = len(items)

    header_size = 7 * 4  # 7 uint32
    entry_size = 8  # (length, offset) = 2 uint32 values

    orig_table_offset = header_size
    trans_table_offset = orig_table_offset + nstrings * entry_size
    string_offset = trans_table_offset + nstrings * entry_size

    # Prepare tables and string data buffer
    orig_table: List[Tuple[int, int]] = []
    trans_table: List[Tuple[int, int]] = []
    string_data = bytearray()

    current_offset = string_offset

    # Pre-encode strings (UTF-8)
    encoded_ids = [msgid.encode("utf-8") for msgid, _ in items]
    encoded_strs = [msgstr.encode("utf-8") for _, msgstr in items]

    # Build original msgid table
    for b_msgid in encoded_ids:
        length = len(b_msgid)
        orig_table.append((length, current_offset))
        string_data.extend(b_msgid + b"\0")
        current_offset += length + 1

    # Build translated msgstr table
    for b_msgstr in encoded_strs:
        length = len(b_msgstr)
        trans_table.append((length, current_offset))
        string_data.extend(b_msgstr + b"\0")
        current_offset += length + 1

    # ----------------------------------------
    # Build final binary output
    # ----------------------------------------
    out = bytearray()

    # Header
    out.extend(
        struct.pack(
            "<IIIIIII",
            magic,
            revision,
            nstrings,
            orig_table_offset,
            trans_table_offset,
            0,  # hash_size
            0,  # hash_offset
        )
    )

    # Original strings table
    for length, offset in orig_table:
        out.extend(struct.pack("<II", length, offset))

    # Translated strings table
    for length, offset in trans_table:
        out.extend(struct.pack("<II", length, offset))

    # Actual string data
    out.extend(string_data)

    # Write file
    path.write_bytes(out)
