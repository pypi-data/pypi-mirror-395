# src/pypomo/utils/cache_manager.py
from __future__ import annotations

import os
from functools import lru_cache
from typing import Callable, Dict, Optional


class PluralExprCache:
    """
    Cache manager for plural expression compilation.

    Supported backends:
      - "none": No caching (always recompile)
      - "weak": Dict-based cache
      - "lru" : LRU cache via functools.lru_cache
    """

    def __init__(self, backend: str = "weak", maxsize: int = 256):
        if backend not in {"none", "weak", "lru"}:
            raise ValueError(f"Unknown cache backend: {backend}")

        self.backend = backend
        self.maxsize = maxsize

        # weak cache uses a normal dict
        self._weak: Dict[str, str] = {}

        # lru cache wraps the compile function
        self._lru_func: Optional[Callable[[str], str]] = None
        if backend == "lru":
            # wrap compile function — the real compiler is injected late
            self._lru_func = lru_cache(maxsize=maxsize)(self._wrap_compile)

        # compiler function is injected from outside
        self._compiler: Optional[Callable[[str], str]] = None

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------
    def set_compiler(self, compiler: Callable[[str], str]) -> None:
        """Inject the real compile function (e.g., _compile_plural_expr)."""
        self._compiler = compiler

    def get_or_compile(
        self,
        expr: str,
        compiler: Callable[[str], str] | None = None,
    ) -> str:
        """
        Return compiled Python expression.
        Uses the specified cache backend.
        """
        key = expr.strip()

        if compiler is not None and self._compiler is None:
            self._compiler = compiler

        c: Callable[[str], str] | None = compiler or self._compiler
        if c is None:
            raise RuntimeError("Compiler not configured")

        # Backend: none
        if self.backend == "none":
            return c(key)

        # Backend: weak dict
        if self.backend == "weak":
            if key in self._weak:
                return self._weak[key]
            compiled = c(key)
            self._weak[key] = compiled
            return compiled

        # Backend: LRU
        assert self._lru_func is not None
        return self._lru_func(key)

    # ---------------------------------------------------
    # Private helper used only for LRU
    # ---------------------------------------------------
    def _wrap_compile(self, expr: str) -> str:
        """Used by LRU backend"""
        if self._compiler is None:
            raise RuntimeError(
                "Should be monkey-patched by PluralRule to call _compile_plural_expr"
            )
        return self._compiler(expr)


# ----------------------------------------
# DEFAULT CACHE FACTORY (環境変数対応)
# ----------------------------------------
def get_default_cache(
    backend: str | None = None,
    maxsize: int | None = None,
    compiler: Callable[[str], str] | None = None,
) -> PluralExprCache:
    """
    Return a PluralExprCache instance based on environment variable:

        PYPOMO_CACHE = none | weak | lru

    Unknown values fall back to "weak".
    """
    backend = backend or os.getenv('PYPOMO_CACHE', 'lru').lower()
    maxsize = maxsize or int(os.getenv('PYPOMO_PLURAL_CACHE_SIZE', "256"))

    if backend not in {"none", "weak", "lru"}:
        backend = "lru"

    cache = PluralExprCache(backend=backend, maxsize=maxsize)

    if compiler is not None:
        cache.set_compiler(compiler)

    return cache
