# src/pypomo/mo/decoder.py

from __future__ import annotations

from typing import Iterable, List

from .types import DecodedItem


def decode_map_pairs(
    ids: List[bytes],
    strs: List[bytes],
    encoding: str = "utf-8",
) -> Iterable[DecodedItem]:
    """
    Convert raw msgid/msgstr byte arrays into text pairs.

    Handles:
        - singular entries
        - plural entries (msgid1\0msgid2)
        - multi-form translations (msgstr1\0msgstr2)

    Output:
        - yields (msgid, msgstr)
        - plural forms are yielded as separate entries:
            (("apple", 0), "apple")
            (("apple", 1), "apples")
    """
    for b_id, b_str in zip(ids, strs):
        # msgid
        if b"\x00" in b_id:
            # plural msgids
            parts = b_id.split(b"\x00")
            msgid_singular = parts[0].decode(encoding, errors="ignore")
            msgid_plural = parts[1].decode(encoding, errors="ignore")

            # msgstr forms
            forms = [
                s.decode(encoding, errors="ignore")
                for s in b_str.split(b"\x00")
            ]

            yield {
                "kind": "plural-header",
                "singular": msgid_singular,
                "plural": msgid_plural,
                "forms": forms,
            }
        else:
            msgid = b_id.decode(encoding, errors="ignore")
            msgstr = b_str.decode(encoding, errors="ignore")
            yield {
                "kind": "single",
                "msgid": msgid,
                "msgstr": msgstr,
            }
