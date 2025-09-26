from tiny_python import tiny_exec


def test_empty_code():
    assert tiny_exec("") is None


def test_whitespace_only():
    assert tiny_exec("   \n  \t  ") is None


def test_pass_statement():
    assert tiny_exec("pass") is None


def test_multiple_pass():
    code = """
pass
pass
pass
"""
    assert tiny_exec(code) is None


def test_multiple_statements_return_last():
    code = """
a = 1
b = 2
c = 3
a + b + c
"""
    assert tiny_exec(code) == 6


def test_no_final_expression():
    code = """
a = 1
b = 2
c = a + b
"""
    assert tiny_exec(code) == 3  # Returns the assignment value


def test_comparison_operators():
    assert tiny_exec("5 > 3")
    assert not tiny_exec("5 < 3")
    assert tiny_exec("5 == 5")
    assert tiny_exec("5 != 3")
    assert tiny_exec("5 >= 5")
    assert tiny_exec("3 <= 5")


def test_chained_comparisons():
    assert tiny_exec("1 < 2 < 3")
    assert not tiny_exec("1 < 2 > 3")
    assert tiny_exec("5 >= 5 == 5")


def test_boolean_operators():
    assert not tiny_exec("True and False")
    assert tiny_exec("True or False")
    assert not tiny_exec("not True")
    assert tiny_exec("not False")


def test_short_circuit_evaluation():
    code = """
result = []
True or result.append(1)
result
"""
    assert tiny_exec(code) == []

    code = """
result = []
False and result.append(1)
result
"""
    assert tiny_exec(code) == []


def test_in_operator():
    assert tiny_exec("3 in [1, 2, 3, 4]")
    assert tiny_exec("5 not in [1, 2, 3, 4]")
    assert tiny_exec("'a' in 'abc'")
    assert tiny_exec("'d' not in 'abc'")


def test_is_operator():
    code = """
x = None
x is None
"""
    assert tiny_exec(code)

    code = """
x = 5
x is not None
"""
    assert tiny_exec(code)


def test_nested_structures():
    code = """
data = {
    "list": [1, 2, 3],
    "dict": {"a": 1, "b": 2},
    "tuple": (4, 5, 6)
}
data["list"][1] + data["dict"]["b"] + data["tuple"][0]
"""
    assert tiny_exec(code) == 8


def test_complex_nesting():
    code = """
matrix = [[1, 2], [3, 4], [5, 6]]
total = 0
for row in matrix:
    for val in row:
        total += val
total
"""
    assert tiny_exec(code) == 21
