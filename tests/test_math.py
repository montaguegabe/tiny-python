from tiny_python import safe_exec


def test_addition():
    assert safe_exec("2 + 3") == 5


def test_subtraction():
    assert safe_exec("10 - 4") == 6


def test_multiplication():
    assert safe_exec("3 * 4") == 12


def test_division():
    assert safe_exec("15 / 3") == 5.0


def test_floor_division():
    assert safe_exec("17 // 5") == 3


def test_modulo():
    assert safe_exec("17 % 5") == 2


def test_power():
    assert safe_exec("2 ** 3") == 8


def test_complex_expression():
    assert safe_exec("2 + 3 * 4 - 1") == 13


def test_parentheses():
    assert safe_exec("(2 + 3) * 4") == 20


def test_negative_numbers():
    assert safe_exec("-5 + 3") == -2
    assert safe_exec("5 * -2") == -10