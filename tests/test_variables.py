from tiny_python import safe_exec


def test_simple_assignment():
    code = """
x = 10
x
"""
    assert safe_exec(code) == 10


def test_multiple_assignments():
    code = """
x = 10
y = 20
z = x + y
z
"""
    assert safe_exec(code) == 30


def test_augmented_assignment():
    code = """
x = 10
x += 5
x *= 2
x
"""
    assert safe_exec(code) == 30


def test_variable_reassignment():
    code = """
x = 5
x = x + 10
x = x * 2
x
"""
    assert safe_exec(code) == 30


def test_tuple_unpacking():
    code = """
t = (1, 2, 3)
a, b, c = t
a + b + c
"""
    assert safe_exec(code) == 6