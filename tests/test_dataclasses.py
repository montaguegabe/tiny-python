from dataclasses import dataclass

from tiny_python import tiny_eval_last


def test_dataclass_instantiation():
    @dataclass
    class Point:
        x: float
        y: float

    code = """
p = Point(3, 4)
p.x + p.y
"""
    result = tiny_eval_last(code, allowed_classes=[Point])
    assert result == 7


def test_dataclass_with_kwargs():
    @dataclass
    class Point:
        x: float
        y: float

    code = """
p = Point(x=5, y=12)
(p.x ** 2 + p.y ** 2) ** 0.5
"""
    result = tiny_eval_last(code, allowed_classes=[Point])
    assert abs(result - 13.0) < 0.01


def test_dataclass_attribute_access():
    @dataclass
    class Person:
        name: str
        age: int

    code = """
p = Person("Alice", 30)
p.name + " is " + str(p.age) + " years old"
"""
    result = tiny_eval_last(code, allowed_classes=[Person])
    assert result == "Alice is 30 years old"
