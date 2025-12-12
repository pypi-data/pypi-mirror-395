# src/pypomo/mo/types.py

from __future__ import annotations

from typing import List, Literal, TypedDict, Union

from typing_extensions import TypeAlias


class SinglePayload(TypedDict):
    kind: Literal["single"]
    msgid: str
    msgstr: str


class PluralPayload(TypedDict):
    kind: Literal["plural-header"]
    singular: str
    plural: str
    forms: List[str]


DecodedItem: TypeAlias = Union[SinglePayload, PluralPayload]
