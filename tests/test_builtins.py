from tiny_python import tiny_eval_last


def test_len():
    assert tiny_eval_last("len([1, 2, 3, 4, 5])") == 5
    assert tiny_eval_last('len("hello")') == 5
    assert tiny_eval_last("len({})") == 0


def test_range():
    code = """
list(range(5))
"""
    assert tiny_eval_last(code) == [0, 1, 2, 3, 4]

    code = """
list(range(2, 7))
"""
    assert tiny_eval_last(code) == [2, 3, 4, 5, 6]

    code = """
list(range(0, 10, 2))
"""
    assert tiny_eval_last(code) == [0, 2, 4, 6, 8]


def test_type_conversions():
    assert tiny_eval_last("int('42')") == 42
    assert tiny_eval_last("float('3.14')") == 3.14
    assert tiny_eval_last("str(123)") == "123"
    assert tiny_eval_last("bool(1)")
    assert not tiny_eval_last("bool(0)")
    assert tiny_eval_last("bool('hello')")
    assert not tiny_eval_last("bool('')")


def test_min_max():
    assert tiny_eval_last("min([3, 1, 4, 1, 5])") == 1
    assert tiny_eval_last("max([3, 1, 4, 1, 5])") == 5
    assert tiny_eval_last("min(3, 1, 4)") == 1
    assert tiny_eval_last("max(3, 1, 4)") == 4


def test_sum():
    assert tiny_eval_last("sum([1, 2, 3, 4, 5])") == 15
    assert tiny_eval_last("sum([])") == 0
    assert tiny_eval_last("sum([1.5, 2.5, 3.0])") == 7.0


def test_abs():
    assert tiny_eval_last("abs(-5)") == 5
    assert tiny_eval_last("abs(5)") == 5
    assert tiny_eval_last("abs(-3.14)") == 3.14


def test_round():
    assert tiny_eval_last("round(3.7)") == 4
    assert tiny_eval_last("round(3.5)") == 4
    assert tiny_eval_last("round(3.14159, 2)") == 3.14


def test_sorted():
    assert tiny_eval_last("sorted([3, 1, 4, 1, 5])") == [1, 1, 3, 4, 5]
    assert tiny_eval_last("sorted([3, 1, 4], reverse=True)") == [4, 3, 1]


def test_reversed():
    assert tiny_eval_last("reversed([1, 2, 3])") == [3, 2, 1]


def test_enumerate():
    code = """
result = []
for i, val in enumerate(['a', 'b', 'c']):
    result.append((i, val))
result
"""
    assert tiny_eval_last(code) == [(0, "a"), (1, "b"), (2, "c")]


def test_zip():
    code = """
list(zip([1, 2, 3], ['a', 'b', 'c']))
"""
    assert tiny_eval_last(code) == [(1, "a"), (2, "b"), (3, "c")]


def test_all_any():
    assert tiny_eval_last("all([True, True, True])")
    assert not tiny_eval_last("all([True, False, True])")
    assert tiny_eval_last("any([False, True, False])")
    assert not tiny_eval_last("any([False, False, False])")


def test_isinstance():
    assert tiny_eval_last("isinstance(5, int)")
    assert tiny_eval_last("isinstance('hello', str)")
    assert tiny_eval_last("isinstance([1, 2], list)")
    assert not tiny_eval_last("isinstance(5, str)")
