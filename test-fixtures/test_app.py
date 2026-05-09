"""Test suite for Calculator - incomplete coverage, bad naming."""

from app import Calculator


def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0


def test_subtract():
    calc = Calculator()
    assert calc.subtract(10, 3) == 7


def test1():
    """Poorly named test - tests divide normal case."""
    calc = Calculator()
    assert calc.divide(10, 2) == 5


def test2():
    """Poorly named test - tests divide with negative."""
    calc = Calculator()
    assert calc.divide(-6, 3) == -2


# MISSING: test_multiply
# MISSING: test_divide_by_zero
# MISSING: test_divide_float
# MISSING: test_search_user_sql_injection
# MISSING: test_calculate_expression_safety
