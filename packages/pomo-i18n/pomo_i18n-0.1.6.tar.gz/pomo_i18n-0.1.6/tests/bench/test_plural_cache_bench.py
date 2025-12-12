# tests/bench/test_plural_cache_bench.py
# type: ignore

import pytest

from pypomo.utils.cache_manager import PluralExprCache
from pypomo.utils.plural_forms import PluralRule

# テスト用の適当な plural expr
EXPR_SIMPLE = "n != 1"
EXPR_COMPLEX = "(n==1)?0:(n>=2 && n<=4)?1:2"


@pytest.mark.parametrize("backend", ["none", "weak", "lru"])
def test_plural_simple_bench(benchmark, backend):
    """backend ごとの単純 plural 呼び出しベンチ"""
    cache = PluralExprCache(backend=backend)
    cache.set_compiler(lambda x: x)  # ダミーのコンパイラ

    rule = PluralRule.from_expression(EXPR_SIMPLE, 2, cache=cache)

    benchmark(lambda: rule(5))


@pytest.mark.parametrize("backend", ["none", "weak", "lru"])
def test_plural_complex_bench(benchmark, backend):
    """backend ごとの複雑 plural 呼び出しベンチ"""
    cache = PluralExprCache(backend=backend)
    cache.set_compiler(lambda x: x)

    rule = PluralRule.from_expression(EXPR_COMPLEX, 3, cache=cache)

    benchmark(lambda: rule(5))
