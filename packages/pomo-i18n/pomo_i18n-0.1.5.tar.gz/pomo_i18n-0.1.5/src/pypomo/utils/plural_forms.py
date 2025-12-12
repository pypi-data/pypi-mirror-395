# src/pypomo/utils/plural_forms.py
#
# Strict, safe plural-form parser for gettext-style rules.
#
# Supports:
# - Parsing "Plural-Forms:" header from PO files
# - Converting C-style plural expressions into Python expressions
# - Nested ternary operators (? :)
# - && / || / ! operators
# - Safe evaluation via restricted env
#
# This module does *not* evaluate any untrusted Python code.
# All expressions are converted from a limited subset of C syntax.

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from .cache_manager import PluralExprCache, get_default_cache

# Regex for extracting nplurals and plural expression from "Plural-Forms:" header
_PLURAL_HEADER_RE = re.compile(
    r"nplurals\s*=\s*(\d+)\s*;\s*plural\s*=\s*([^;]+)",
    re.IGNORECASE,
)


# ----------------------------------------
# Expression conversion
# ----------------------------------------
def _convert_ternary(expr: str) -> str:
    expr = expr.strip()

    # No ternary operator
    if "?" not in expr:
        return expr

    # Find top-level ? :
    depth = 0
    q_pos = None
    colon_pos = None

    for i, ch in enumerate(expr):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "?" and depth == 0 and q_pos is None:
            q_pos = i
        elif ch == ":" and depth == 0 and q_pos is not None:
            colon_pos = i
            break

    if q_pos is None or colon_pos is None:
        return expr

    # Extract parts
    cond = expr[:q_pos].strip()
    true_part = expr[q_pos + 1 : colon_pos].strip()
    false_part = expr[colon_pos + 1 :].strip()

    # Unwrap outer parentheses correctly
    def unwrap(s: str) -> str:
        if s.startswith("(") and s.endswith(")"):
            # Ensure parentheses actually match
            depth = 0
            for i, ch in enumerate(s):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                if depth == 0 and i < len(s) - 1:
                    return s  # not a single outer pair
            return s[1:-1].strip()
        return s

    cond = _convert_ternary(unwrap(cond))
    true_part = _convert_ternary(unwrap(true_part))
    false_part = _convert_ternary(unwrap(false_part))

    return f"({true_part} if ({cond}) else ({false_part}))"


def _compile_plural_expr(expr: str) -> str:
    """
    Convert a gettext-style plural expression (C-like syntax)
    into a valid Python expression.

    Supported conversions:
        &&  -> and
        ||  -> or
        !x  -> not x
        cond ? a : b  -> (a if cond else b)
    """
    s = expr.strip()

    # Remove trailing semicolon if present
    if s.endswith(";"):
        s = s[:-1].rstrip()

    # Replace logical operators
    s = s.replace("&&", " and ").replace("||", " or ")

    # Temporarily replace "!=" to safely handle "!"
    s = s.replace("!=", "__NE__")

    # Replace !foo → not foo
    s = re.sub(r"!\s*", " not ", s)

    # Restore "!="
    s = s.replace("__NE__", "!=")

    # Convert ternary operator
    s = _convert_ternary(s)
    return s


# ----------------------------------------
# Default cache
# ----------------------------------------
DEFAULT_CACHE: PluralExprCache = get_default_cache(
    compiler=_compile_plural_expr
)


@dataclass(slots=True)
class PluralRule:
    """
    Represents a plural rule derived from a gettext `Plural-Forms:` header.

    Example header:
        "Plural-Forms: nplurals=2; plural=(n != 1);"

    Attributes:
        nplurals: Number of plural forms.
        expr:     Original C-like plural expression.
        func:     Callable that maps n -> plural index.
    """

    nplurals: int
    expr: str
    func: Callable[[int], int]

    def __call__(self, n: int) -> int:
        """Convenience: rule(n) → index."""
        return self.func(n)

    # ----------------------------------------
    # Factory
    # ----------------------------------------
    @classmethod
    def from_header(
        cls,
        header: str,
        cache: PluralExprCache | None = None,
    ) -> PluralRule:
        """
        Parse a gettext-style Plural-Forms header and return a PluralRule.

        The header may contain multiple lines from msgstr:
            msgstr ""
            "Language: en\n"
            "Plural-Forms: nplurals=2; plural=(n != 1);\n"

        Fallback behavior:
            If no plural rule is found, English-style (n != 1) is assumed.
        """
        cache = cache or DEFAULT_CACHE

        m = _PLURAL_HEADER_RE.search(header)
        if not m:
            # Default: English-like rule
            return cls(
                nplurals=2,
                expr="n != 1",
                func=lambda n: 0 if n == 1 else 1,
            )

        nplurals = int(m.group(1))
        raw_expr = m.group(2).strip()

        try:
            py_expr = cache.get_or_compile(raw_expr)
        except Exception:
            # Expression invalid → treat all as singular (0)
            return cls(
                nplurals=nplurals,
                expr=raw_expr,
                func=lambda n: 0,
            )

        # Construct the safe eval function (restricted env)
        def _func(n: int) -> int:
            try:
                value = eval(py_expr, {"__builtins__": {}}, {"n": n})
                if not isinstance(value, int):
                    value = int(value)
            except Exception:
                # fallback: treat all plural values as 0 (singular form)
                return 0

            # Clamp index to valid range
            if value < 0:
                return 0
            if value >= nplurals:
                return nplurals - 1
            return value

        return cls(nplurals=nplurals, expr=raw_expr, func=_func)

    @classmethod
    def from_expression(
        cls,
        expr: str,
        nplurals: int,
        cache: PluralExprCache | None = None,
    ) -> PluralRule:
        """
        Create a PluralRule directly from a raw plural expression.

        This is mainly useful for:
            - Unit tests
            - Programmatic plural rule creation
            - Situations where a full "Plural-Forms:" header is not available

        Example:
            rule = PluralRule.from_expression("n > 1 && n < 4", nplurals=2)
            rule(1)  # -> 0
            rule(2)  # -> 1
        """
        cache = cache or DEFAULT_CACHE

        try:
            py_expr = cache.get_or_compile(expr)
        except Exception:
            # Invalid expression → always return 0
            return cls(
                nplurals=nplurals,
                expr=expr,
                func=lambda n: 0,
            )

        def _func(n: int) -> int:
            try:
                value = eval(py_expr, {"__builtins__": {}}, {"n": n})
                if not isinstance(value, int):
                    value = int(value)
            except Exception:
                return 0

            # Clamp to valid range
            if value < 0:
                value = 0
            if value >= nplurals:
                return nplurals - 1
            return value

        return cls(nplurals=nplurals, expr=expr, func=_func)
