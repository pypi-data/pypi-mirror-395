# tests/test_plural_rule_eval.py
# type: ignore

from pypomo.utils.plural_forms import PluralRule

# ----------------------------------------
# Basic operators
# ----------------------------------------


def test_operator_and_or_not():
    rule = PluralRule.from_expression("n > 1 && n < 4", nplurals=2)
    assert rule(2) == 1
    assert rule(3) == 1
    assert rule(1) == 0
    assert rule(5) == 0

    rule2 = PluralRule.from_expression("!(n == 1)", nplurals=2)
    assert rule2(1) == 0
    assert rule2(2) == 1


def test_ternary_basic():
    rule = PluralRule.from_expression(
        "n == 1 ? 0 : (n > 4 ? 2 : 1)",
        nplurals=3,
    )
    assert rule(1) == 0
    assert rule(2) == 1
    assert rule(3) == 1
    assert rule(5) == 2


# ----------------------------------------
# Language-specific plural rules
# ----------------------------------------


def test_plural_english():
    rule = PluralRule.from_expression("n != 1", nplurals=2)
    assert rule(1) == 0
    assert rule(2) == 1
    assert rule(0) == 1


def test_plural_japanese():
    rule = PluralRule.from_expression("0", nplurals=1)
    for n in range(0, 20):
        assert rule(n) == 0


def test_plural_russian():
    rule = PluralRule.from_expression(
        "n%10==1 && n%100!=11 ? 0 : "
        "(n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)",
        nplurals=3,
    )
    assert rule(1) == 0
    assert rule(2) == 1
    assert rule(4) == 1
    assert rule(5) == 2
    assert rule(11) == 2
    assert rule(21) == 0


def test_plural_french():
    rule = PluralRule.from_expression(
        "n > 1",
        nplurals=2,
    )
    assert rule(0) == 0
    assert rule(1) == 0
    assert rule(2) == 1


def test_plural_polish():
    rule = PluralRule.from_expression(
        "n==1 ? 0 : (n%10>=2 && n%10<=4 "
        "&& (n%100<10 || n%100>=20) ? 1 : 2)",
        nplurals=3,
    )
    assert rule(1) == 0
    assert rule(2) == 1
    assert rule(5) == 2


# ----------------------------------------
# Header parsing
# ----------------------------------------


def test_from_header_valid():
    header = "Language: en\nPlural-Forms: nplurals=2; plural=(n != 1);\n"
    rule = PluralRule.from_header(header)
    assert rule.nplurals == 2
    assert rule(1) == 0
    assert rule(2) == 1


def test_from_header_missing_plural():
    header = "Language: xx\nPlural-Forms: nplurals=3;\n"
    rule = PluralRule.from_header(header)

    # fallback → english rule (n != 1)
    assert rule.nplurals == 2
    assert rule(1) == 0
    assert rule(2) == 1


def test_from_header_invalid_expr():
    header = "Plural-Forms: nplurals=2; plural=INVALID_EXPRESSION;\n"
    rule = PluralRule.from_header(header)
    # Expect fallback: treat all as singular (0)
    assert rule(99) == 0


# ----------------------------------------
# Edge cases
# ----------------------------------------


def test_negative_numbers():
    rule = PluralRule.from_expression("n != 1", nplurals=2)
    assert rule(-1) == 1
    assert rule(-100) == 1


def test_large_numbers():
    rule = PluralRule.from_expression("n > 1", 2)
    assert rule(1000000) == 1
