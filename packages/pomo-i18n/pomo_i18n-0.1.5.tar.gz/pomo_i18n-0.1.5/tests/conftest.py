# tests/conftest.py

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pytest


@pytest.fixture
def write_po(tmp_path: Path):
    """
    Helper fixture to create a .po file under a temp directory.

    Usage:
        path = write_po("messages", "en", content_lines)
    """

    def _write_po(domain: str, lang: str, lines: Iterable[str]) -> Path:
        base = tmp_path / "locales" / lang / "LC_MESSAGES"
        base.mkdir(parents=True, exist_ok=True)
        po_path = base / f"{domain}.po"
        po_path.write_text("\n".join(lines), encoding="utf-8")
        return po_path

    return _write_po
