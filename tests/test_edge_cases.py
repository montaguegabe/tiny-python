from tiny_python import safe_exec


def test_empty_code():
    assert safe_exec("") is None


def test_whitespace_only():
    assert safe_exec("   \n  \t  ") is None


def test_pass_statement():
    assert safe_exec("pass") is None


def test_multiple_pass():
    code = """
pass
pass
pass
"""
    assert safe_exec(code) is None


def test_multiple_statements_return_last():
    code = """
a = 1
b = 2
c = 3
a + b + c
"""
    assert safe_exec(code) == 6


def test_no_final_expression():
    code = """
a = 1
b = 2
c = a + b
"""
    assert safe_exec(code) == 3  # Returns the assignment value


def test_comparison_operators():
    assert safe_exec("5 > 3")
    assert not safe_exec("5 < 3")
    assert safe_exec("5 == 5")
    assert safe_exec("5 != 3")
    assert safe_exec("5 >= 5")
    assert safe_exec("3 <= 5")


def test_chained_comparisons():
    assert safe_exec("1 < 2 < 3")
    assert not safe_exec("1 < 2 > 3")
    assert safe_exec("5 >= 5 == 5")


def test_boolean_operators():
    assert not safe_exec("True and False")
    assert safe_exec("True or False")
    assert not safe_exec("not True")
    assert safe_exec("not False")


def test_short_circuit_evaluation():
    code = """
result = []
True or result.append(1)
result
"""
    assert safe_exec(code) == []

    code = """
result = []
False and result.append(1)
result
"""
    assert safe_exec(code) == []


def test_in_operator():
    assert safe_exec("3 in [1, 2, 3, 4]")
    assert safe_exec("5 not in [1, 2, 3, 4]")
    assert safe_exec("'a' in 'abc'")
    assert safe_exec("'d' not in 'abc'")


def test_is_operator():
    code = """
x = None
x is None
"""
    assert safe_exec(code)

    code = """
x = 5
x is not None
"""
    assert safe_exec(code)


def test_nested_structures():
    code = """
data = {
    "list": [1, 2, 3],
    "dict": {"a": 1, "b": 2},
    "tuple": (4, 5, 6)
}
data["list"][1] + data["dict"]["b"] + data["tuple"][0]
"""
    assert safe_exec(code) == 8


def test_complex_nesting():
    code = """
matrix = [[1, 2], [3, 4], [5, 6]]
total = 0
for row in matrix:
    for val in row:
        total += val
total
"""
    assert safe_exec(code) == 21