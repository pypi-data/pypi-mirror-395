# src/pypomo/parser/types.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class POEntry:
    msgid: str
    msgstr: str = field(default="")
    msgid_plural: str | None = field(default=None)
    msgstr_plural: Dict[int, str] = field(default_factory=dict[int, str])
    comments: List[str] = field(default_factory=list[str])
    extracted_comments: List[str] = field(default_factory=list[str])
    references: List[str] = field(default_factory=list[str])
    flags: List[str] = field(default_factory=list[str])
