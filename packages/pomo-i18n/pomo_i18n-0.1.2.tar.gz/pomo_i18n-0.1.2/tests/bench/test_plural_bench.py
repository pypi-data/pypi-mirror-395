# tests/bench/test_plural_bench.py
# type: ignore

from __future__ import annotations

from pypomo.utils.plural_forms import PluralRule


def test_plural_call_benchmark(benchmark):
    rule = PluralRule.from_expression("n != 1", nplurals=2)
    benchmark(lambda: rule(5))


def test_complex_plural_benchmark(benchmark):
    rule = PluralRule.from_expression(
        "(n%10==1 && n%100!=11 ? 0 : n!=0 ? 1 : 2)", nplurals=3
    )
    benchmark(lambda: rule(123))
