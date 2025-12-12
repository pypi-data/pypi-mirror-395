# bench/timeit_plural.py
# type: ignore

import timeit

from pypomo.utils.plural_forms import PluralRule

# Prepare rule once (global)
rule = PluralRule.from_expression("n != 1", 2)

# Prepare complex rule (global)
complex_rule = PluralRule.from_expression(
    "(n==1)?0:(n>=2 && n<=4)?1:2",
    3,
)


def bench_plural_call():
    stmt = "rule(5)"
    setup = "from __main__ import rule"

    loops = 100000
    t = timeit.timeit(stmt, setup=setup, number=loops)
    print(f"plural call: {t:.6f} sec for {loops} loops")


def bench_complex():
    stmt = "rule2(5)"
    setup = "from __main__ import complex_rule as rule2"

    loops = 100000
    t = timeit.timeit(stmt, setup=setup, number=loops)
    print(f"complex plural: {t:.6f} sec for {loops} loops")


if __name__ == "__main__":
    print("=== Timeit micro benchmarks ===")
    bench_plural_call()
    bench_complex()
