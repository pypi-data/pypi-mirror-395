# src/pypomo/parser/po_parser.py

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

from .types import POEntry


class POParser:
    """
    Strict-mypy compatible .po parser.

    Supports:
    - msgid / msgstr
    - plural: msgid_plural / msgstr[n]
    - multiline strings
    - comments (#, #., #:, #,)
    """

    def parse(self, path: str | Path) -> List[POEntry]:
        path = Path(path)
        lines = path.read_text(encoding="utf-8").splitlines()

        entries: List[POEntry] = []
        current: Optional[POEntry] = None
        current_field: str | None = None  # "msgid", "msgstr", etc.

        def commit() -> None:
            nonlocal current
            nonlocal current_field
            if current is not None:
                entries.append(current)
                current = None
            current_field = None

        def strip_quotes(s: str) -> str:
            s = s.strip()
            if s.startswith('"') and s.endswith('"'):
                return s[1:-1]
            return s

        for raw in lines:
            line = raw.strip()

            # Empty → commit
            if not line:
                continue

            # Comments
            if line.startswith("#"):
                if current is None:
                    current = POEntry(msgid="")
                current.comments.append(line)
                continue

            # msgid
            if line.startswith("msgid "):
                commit()
                text = strip_quotes(line[5:].strip())
                current = POEntry(msgid=text)
                current_field = "msgid"
                continue

            # msgid_plural
            if line.startswith("msgid_plural "):
                if current is None:
                    raise ValueError("msgid_plural without msgid")
                text = strip_quotes(line[len("msgid_plural ") :].strip())
                current.msgid_plural = text
                current_field = "msgid_plural"
                continue

            # msgstr (singular)
            if line.startswith("msgstr "):
                if current is None:
                    raise ValueError("msgstr without msgid")
                text = strip_quotes(line[6:].strip())
                current.msgstr = text
                current_field = "msgstr"
                continue

            # msgstr[n]
            if line.startswith("msgstr["):
                if current is None:
                    raise ValueError("msgstr[n] without msgid")

                # the format of "msgstr[0] 'apple'"
                #  -> Parse robustly with regular expressions
                m = re.match(r'msgstr\[(\d+)\]\s+"(.*)"', line)
                if m:
                    idx = int(m.group(1))
                    text = m.group(2)
                    current.msgstr_plural[idx] = text
                    current_field = f"msgstr_plural[{idx}]"
                    continue

                # fallback
                idx = int(line[len("msgstr[") : line.index("]")])
                text = strip_quotes(line[line.index("]") + 1 :].strip())
                current.msgstr_plural[idx] = text
                current_field = f"msgstr_plural[{idx}]"
                continue

            # Multiline
            if line.startswith('"') and line.endswith('"'):
                if current is None or current_field is None:
                    raise ValueError("Multiline string without context")

                text = strip_quotes(line)
                if current_field == "msgid":
                    current.msgid += text
                elif current_field == "msgid_plural":
                    current.msgid_plural = (current.msgid_plural or "") + text
                elif current_field == "msgstr":
                    current.msgstr += text
                elif current_field.startswith("msgstr_plural"):
                    idx = int(current_field.split("[")[1].split("]")[0])
                    current.msgstr_plural[idx] = (
                        current.msgstr_plural.get(idx, "") + text
                    )
                continue

            # Anything else = ignore or future extension
            continue

        commit()
        return entries
