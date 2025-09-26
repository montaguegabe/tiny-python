from tiny_python import tiny_eval_last


def test_addition():
    assert tiny_eval_last("2 + 3") == 5


def test_subtraction():
    assert tiny_eval_last("10 - 4") == 6


def test_multiplication():
    assert tiny_eval_last("3 * 4") == 12


def test_division():
    assert tiny_eval_last("15 / 3") == 5.0


def test_floor_division():
    assert tiny_eval_last("17 // 5") == 3


def test_modulo():
    assert tiny_eval_last("17 % 5") == 2


def test_power():
    assert tiny_eval_last("2 ** 3") == 8


def test_complex_expression():
    assert tiny_eval_last("2 + 3 * 4 - 1") == 13


def test_parentheses():
    assert tiny_eval_last("(2 + 3) * 4") == 20


def test_negative_numbers():
    assert tiny_eval_last("-5 + 3") == -2
    assert tiny_eval_last("5 * -2") == -10
