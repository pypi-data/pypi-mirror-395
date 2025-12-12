# src/pypomo/mo/binary_reader.py

from __future__ import annotations

import struct
from pathlib import Path
from typing import Dict, List, Tuple


def read_mo_binary(
    path: Path,
) -> Tuple[Dict[str, str], List[bytes], List[bytes]]:
    """
    Read a GNU gettext .mo file and return:

        header_info: dict parsed from msgid=""
        ids:  list of raw msgid bytes
        strs: list of raw msgstr bytes

    No decoding is done here — this file only reads binary structure.

    GNU .mo Format:
        magic, revision, nstrings,
        orig_table_ofs, trans_table_ofs,
        hash_size, hash_offset

    Each table contains pairs of (length, offset).
    """
    data = path.read_bytes()

    # Little-endian header
    (
        magic,
        revisions,
        nstrings,
        orig_offset,
        trans_offset,
        hash_size,
        hash_offset,
    ) = struct.unpack("<IIIIIII", data[:28])

    if magic not in (0x950412DE, 0xDE120495):
        raise ValueError("Invalid mo magic number")

    # Read original msgid offsets
    ids: list[bytes] = []
    strs: list[bytes] = []

    for i in range(nstrings):
        length, offset = struct.unpack(
            "<II", data[orig_offset + i * 8 : orig_offset + i * 8 + 8]
        )
        ids.append(data[offset : offset + length])

        length2, offset2 = struct.unpack(
            "<II", data[trans_offset + i * 8 : trans_offset + i * 8 + 8]
        )
        strs.append(data[offset2 : offset2 + length2])

    # Parse header (id == b"")
    header_info: Dict[str, str] = {}
    if ids and ids[0] == b"":
        # Split header lines
        for raw_line in strs[0].split(b"\n"):
            line = raw_line.decode("utf-8", errors="ignore").strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            header_info[key.lower().strip()] = value.strip()

    return header_info, ids, strs
