from tiny_python import tiny_eval_last


def test_empty_code():
    assert tiny_eval_last("") is None


def test_whitespace_only():
    assert tiny_eval_last("   \n  \t  ") is None


def test_pass_statement():
    assert tiny_eval_last("pass") is None


def test_multiple_pass():
    code = """
pass
pass
pass
"""
    assert tiny_eval_last(code) is None


def test_multiple_statements_return_last():
    code = """
a = 1
b = 2
c = 3
a + b + c
"""
    assert tiny_eval_last(code) == 6


def test_no_final_expression():
    code = """
a = 1
b = 2
c = a + b
"""
    assert tiny_eval_last(code) == 3  # Returns the assignment value


def test_comparison_operators():
    assert tiny_eval_last("5 > 3")
    assert not tiny_eval_last("5 < 3")
    assert tiny_eval_last("5 == 5")
    assert tiny_eval_last("5 != 3")
    assert tiny_eval_last("5 >= 5")
    assert tiny_eval_last("3 <= 5")


def test_chained_comparisons():
    assert tiny_eval_last("1 < 2 < 3")
    assert not tiny_eval_last("1 < 2 > 3")
    assert tiny_eval_last("5 >= 5 == 5")


def test_boolean_operators():
    assert not tiny_eval_last("True and False")
    assert tiny_eval_last("True or False")
    assert not tiny_eval_last("not True")
    assert tiny_eval_last("not False")


def test_short_circuit_evaluation():
    code = """
result = []
True or result.append(1)
result
"""
    assert tiny_eval_last(code) == []

    code = """
result = []
False and result.append(1)
result
"""
    assert tiny_eval_last(code) == []


def test_in_operator():
    assert tiny_eval_last("3 in [1, 2, 3, 4]")
    assert tiny_eval_last("5 not in [1, 2, 3, 4]")
    assert tiny_eval_last("'a' in 'abc'")
    assert tiny_eval_last("'d' not in 'abc'")


def test_is_operator():
    code = """
x = None
x is None
"""
    assert tiny_eval_last(code)

    code = """
x = 5
x is not None
"""
    assert tiny_eval_last(code)


def test_nested_structures():
    code = """
data = {
    "list": [1, 2, 3],
    "dict": {"a": 1, "b": 2},
    "tuple": (4, 5, 6)
}
data["list"][1] + data["dict"]["b"] + data["tuple"][0]
"""
    assert tiny_eval_last(code) == 8


def test_complex_nesting():
    code = """
matrix = [[1, 2], [3, 4], [5, 6]]
total = 0
for row in matrix:
    for val in row:
        total += val
total
"""
    assert tiny_eval_last(code) == 21
