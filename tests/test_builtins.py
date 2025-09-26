from tiny_python import safe_exec


def test_len():
    assert safe_exec("len([1, 2, 3, 4, 5])") == 5
    assert safe_exec('len("hello")') == 5
    assert safe_exec("len({})") == 0


def test_range():
    code = """
list(range(5))
"""
    assert safe_exec(code) == [0, 1, 2, 3, 4]

    code = """
list(range(2, 7))
"""
    assert safe_exec(code) == [2, 3, 4, 5, 6]

    code = """
list(range(0, 10, 2))
"""
    assert safe_exec(code) == [0, 2, 4, 6, 8]


def test_type_conversions():
    assert safe_exec("int('42')") == 42
    assert safe_exec("float('3.14')") == 3.14
    assert safe_exec("str(123)") == "123"
    assert safe_exec("bool(1)")
    assert not safe_exec("bool(0)")
    assert safe_exec("bool('hello')")
    assert not safe_exec("bool('')")


def test_min_max():
    assert safe_exec("min([3, 1, 4, 1, 5])") == 1
    assert safe_exec("max([3, 1, 4, 1, 5])") == 5
    assert safe_exec("min(3, 1, 4)") == 1
    assert safe_exec("max(3, 1, 4)") == 4


def test_sum():
    assert safe_exec("sum([1, 2, 3, 4, 5])") == 15
    assert safe_exec("sum([])") == 0
    assert safe_exec("sum([1.5, 2.5, 3.0])") == 7.0


def test_abs():
    assert safe_exec("abs(-5)") == 5
    assert safe_exec("abs(5)") == 5
    assert safe_exec("abs(-3.14)") == 3.14


def test_round():
    assert safe_exec("round(3.7)") == 4
    assert safe_exec("round(3.5)") == 4
    assert safe_exec("round(3.14159, 2)") == 3.14


def test_sorted():
    assert safe_exec("sorted([3, 1, 4, 1, 5])") == [1, 1, 3, 4, 5]
    assert safe_exec("sorted([3, 1, 4], reverse=True)") == [4, 3, 1]


def test_reversed():
    assert safe_exec("reversed([1, 2, 3])") == [3, 2, 1]


def test_enumerate():
    code = """
result = []
for i, val in enumerate(['a', 'b', 'c']):
    result.append((i, val))
result
"""
    assert safe_exec(code) == [(0, "a"), (1, "b"), (2, "c")]


def test_zip():
    code = """
list(zip([1, 2, 3], ['a', 'b', 'c']))
"""
    assert safe_exec(code) == [(1, "a"), (2, "b"), (3, "c")]


def test_all_any():
    assert safe_exec("all([True, True, True])")
    assert not safe_exec("all([True, False, True])")
    assert safe_exec("any([False, True, False])")
    assert not safe_exec("any([False, False, False])")


def test_isinstance():
    assert safe_exec("isinstance(5, int)")
    assert safe_exec("isinstance('hello', str)")
    assert safe_exec("isinstance([1, 2], list)")
    assert not safe_exec("isinstance(5, str)")


def test_type():
    code = """
type(5).__name__
"""
    assert safe_exec(code) == "int"

    code = """
type("hello").__name__
"""
    assert safe_exec(code) == "str"