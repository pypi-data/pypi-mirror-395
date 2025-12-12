# pomo-i18n API Reference

This document provides a structured overview of the public API surface of `pomo-i18n`.
It is intended for users who need deeper details beyond the README.

---

## Table of Contents

- [Catalog](#catalog)
- [Gettext API](#gettext-api)
- [PO Parsing](#po-parsing)
- [MO Writing](#mo-writing)
- [MO Loading](#mo-loading)
- [Plural Rules](#plural-rules)
- [Cache Manager](#cache-manager)
- [Types](#types)

---

## Catalog

```python
from pypomo.catalog import Catalog
```

The central data structure of `pomo-i18n`.
Represents an in-memory translation catalog.

### Creating a Catalog

```python
cat = Catalog()
```

### Building from PO entries

```python
from pypomo.parser.types import POEntry
Catalog.from_po_entries(entries)
```

### Lookup

| Method                                                | Description                                     |
| ----------------------------------------------------- | ----------------------------------------------- |
| `gettext(msgid: str) -> str`                          | Resolve a singular translation                  |
| `ngettext(singular: str, plural: str, n: int) -> str` | Resolve a plural translation using plural rules |

### Updating / merging

| Method                            | Description                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| `merge(other: Catalog) -> None`   | Merge another Catalog into this one, including header, singular, and plural entries. |
| `header_msgstr() -> str`          | Return header raw msgstr                                                             |
| `nplurals: int \| None`           | Number of plural forms                                                               |
| `plural_rule: PluralRule \| None` | PluralRule instance                                                                  |

---

## Gettext API

```python
from pypomo.gettext import gettext, ngettext, translation
```

### translation

```python
translation(
    domain: str,
    localedir: str,
    languages: list[str] | None = None,
) -> Catalog
```

Loads `.po` files into a new Catalog, similar to `gettext.translation`.

### Gettext-style shorthand

```python
from pypomo.gettext import translation

t = translation("messages", "locales", ["en"])
_ = t.gettext  # traditional gettext alias

print(_("Hello"))
```

The name `_` is commonly used as a shorthand alias for gettext in many
Python projects.
Using a local binding ( `_ = t.gettext` ) is safe and recommended.

### Global lookup helpers

- `gettext(msgid: str) -> str`
- `ngettext(singular: str, plural: str, n: int) -> str`

These use the default global catalog.

---

## PO Parsing

Entry point:

```python
from pypomo.parser.po_parser import POParser
```

Features:

- Supports msgid, msgstr
- Supports plural msgid_plural / msgstr[n]
- Extracts header metadata
- Supports gettext-style comments

Output type:

```python
from pypomo.parser.types import POEntry
```

---

## MO Writing

```python
from pypomo.mo.writer import write_mo
```

### write_mo

```python
write_mo(
	path: str | Path,
	catalog: Catalog
) -> None
```

Writes a Catalog to a valid GNU `.mo` file.

Supports:

- sorted msgid table
- UTF-8 encoding
- null-terminated binary format
- plural msgid/msgstr forms

---

## MO Loading

```python
from pypomo.mo.loader import load_mo
```

### load_mo

```python
load_mo(
	path: str | Path
) -> Catalog
```

Loads a `.mo` file into a new Catalog.

Steps internally:

1. binary reading
2. decode msgid/msgstr
3. convert to structured entries
4. build Catalog

---

## Plural Rules

```python
from pypomo.utils.plural_forms import PluralRule
```

Responsible for evaluating C-style plural rules.

---

## Cache Manager

```python
from pypomo.utils.cache_manager import get_default_cache
```

Backends:

- `"none"`
- `"weak"`
- `"lru"` (default)

---

## Types

### POEntry

Structure representing parsed `.po` entries.

### CatalogMessage

Internal normalized message structure.

---

## End of document
