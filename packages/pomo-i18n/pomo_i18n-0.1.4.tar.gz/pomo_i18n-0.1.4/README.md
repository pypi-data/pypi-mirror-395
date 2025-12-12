# pomo-i18n

**English** | [日本語](README.ja.md)

![Tests](https://github.com/kimikato/pomo-i18n/actions/workflows/tests.yml/badge.svg?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/pomo-i18n.svg)](https://pypi.org/project/pomo-i18n/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal, strictly-typed gettext-compatible internationalization library for Python.

`pomo-i18n` provides `.po` and `.mo` parsing, safe plural-form evaluation, and a clean Pythonic API (`gettext`, `ngettext`, `translation`) — all without external dependencies.

---

## Features

- ✔ Parse **`.po`** _and_ **`.mo`** files (GNU gettext format)
- ✔ Full plural-forms support (`Plural-Forms:` header)
- ✔ Safe plural expression evaluator (C-style → Python AST)
- ✔ Strict typing (mypy / Pylance friendly)
- ✔ Pure Python, no external libraries
- ✔ Works on Linux / macOS / Windows

---

## Installation

```sh
pip install pomo-i18n
```

Or vendor it directly:

```
src/
 └─ pypomo/
```

---

## Documentation

- [API Reference](docs/api.md)
- [Benchmark Results](docs/benchmarks.md)

---

## Quick Example

```python
from pypomo.gettext import translation

t = translation(
    domain="messages",
    localedir="locales",
    languages=["en"],
)

_ = t.gettext

print(_("Hello"))
print(t.ngettext("apple", "apples", 1))
print(t.ngettext("apple", "apples", 3))
```

Expected directory layout:

```
locales/
 └─ en/
     └─ LC_MESSAGES/
         └─ messages.po
```

---

## `.po` Parsing

`pomo-i18n` contains a robust standalone `.po` parser:

- `msgid`, `msgstr`
- plurals ( `msgid_plural`, `msgstr[n]` )
- multiline strings
- Supports standard gettext comments:

  - `#` (translator comments)
  - `#.` (extracted comments)
  - `#:` (source references)
  - `#, flags` (parsed as regular comments; `fuzzy` will be supported in a future release)

- header extraction (`msgid ""`)

---

## `.mo` Writing

Compile a Catalog into a `.mo` file:

```python
from pypomo.catalog import Catalog
from pypomo.mo.writer import write_mo
from pypomo.parser.types import POEntry

entries = [
    POEntry(
        msgid="",
        msgstr=(
            "Language: en\n"
            "Plural-Forms: nplurals=2; plural=(n != 1);\n"
        ),
        msgid_plural=None,
        msgstr_plural={},
        comments=[],
    ),
    POEntry("Hello", "Hello!", None, {}, []),
]

cat = Catalog.from_po_entries(entries)
write_mo("messages.mo", cat)
```

The generated `.mo` file is fully compatible with Python’s built-in `gettext.GNUTranslations`.

---

## `.mo` Loading

`pomo-i18n` can also load GNU gettext `.mo` files back into a `Catalog`:

```python
from pypomo.mo.loader import load_mo

cat = load_mo("messages.mo")

_ = cat.gettext
print(_("Hello"))
```

Features:

- verifies magic number (0x9504120E)
- parses msgid/msgstr tables
- handles plural entries correctly
- extracts `Plural-Forms:` from the header

---

## Plural Forms

`pomo-i18n` safely evaluates C-style plural rules:

Example:

```
Plural-Forms: nplurals=2; plural=(n != 1);
```

Russian example:

```
Plural-Forms: nplurals=3;
 plural=(n%10==1 && n%100!=11 ? 0 :
        n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);
```

Expressions are converted to safe Python AST and evaluated with an isolated environment.

---

## Benchmarks

Plural-rule evaluation is optimized and supports multiple cache backends:

- **none** — debugging only
- **weak** — dict-based cache
- **lru** — fastest (default)

Set via environment variable:

```sh
export PYPOMO_CACHE=lru
export PYPOMO_PLURAL_CACHE_SIZE=512
```

---

## Roadmap

- Message merging & locale fallbacks
- Richer comment parsing (`#, fuzzy`, `#.` extracted tags)
- CLI utilities for generating `.pot` files
- Locale auto-detection helpers

---

## License

MIT License
© 2025 Kiminori Kato

---
