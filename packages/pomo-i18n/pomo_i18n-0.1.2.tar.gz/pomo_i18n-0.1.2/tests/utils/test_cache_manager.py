# tests/utils/test_cache_manager.py
# type: ignore

import pytest

from pypomo.utils.cache_manager import PluralExprCache


def test_backend_none_calls_compiler_every_time():
    called = 0

    def compiler(expr: str) -> str:
        nonlocal called
        called += 1
        return f"X:{expr}"

    cache = PluralExprCache("none")
    cache.set_compiler(compiler)

    assert cache.get_or_compile("a", compiler) == "X:a"
    assert cache.get_or_compile("a", compiler) == "X:a"
    assert called == 2


def test_backend_weak_uses_cache():
    called = 0

    def compiler(expr: str) -> str:
        nonlocal called
        called += 1
        return f"Y:{expr}"

    cache = PluralExprCache("weak")
    cache.set_compiler(compiler)

    assert cache.get_or_compile("b", compiler) == "Y:b"
    assert cache.get_or_compile("b", compiler) == "Y:b"
    assert called == 1  # cached!


def test_backend_lru_eviction():
    called = 0

    def compiler(expr: str) -> str:
        nonlocal called
        called += 1
        return f"Z:{expr}"

    cache = PluralExprCache("lru", maxsize=1)
    cache.set_compiler(compiler)

    cache.get_or_compile("c1", compiler)
    cache.get_or_compile("c2", compiler)
    cache.get_or_compile("c1", compiler)

    # eviction が起きるのでコンパイル回数は 3 回になる
    assert called == 3
