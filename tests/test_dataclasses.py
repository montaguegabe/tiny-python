from dataclasses import dataclass

from tiny_python import safe_exec


def test_dataclass_instantiation():
    @dataclass
    class Point:
        x: float
        y: float

    code = """
p = Point(3, 4)
p.x + p.y
"""
    result = safe_exec(code, allowed_classes=[Point])
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
    result = safe_exec(code, allowed_classes=[Point])
    assert abs(result - 13.0) < 0.01


def test_dataclass_with_methods():
    @dataclass
    class Rectangle:
        width: float
        height: float

        def area(self):
            return self.width * self.height

        def perimeter(self):
            return 2 * (self.width + self.height)

    code = """
rect = Rectangle(10, 20)
rect.area()
"""
    assert safe_exec(code, allowed_classes=[Rectangle], allow_dataclass_methods=True) == 200

    code = """
rect = Rectangle(10, 20)
rect.perimeter()
"""
    assert safe_exec(code, allowed_classes=[Rectangle], allow_dataclass_methods=True) == 60


def test_multiple_dataclasses():
    @dataclass
    class Point:
        x: float
        y: float

    @dataclass
    class Circle:
        center: Point
        radius: float

        def area(self):
            return 3.14159 * self.radius**2

    code = """
p = Point(0, 0)
c = Circle(p, 5)
c.area()
"""
    result = safe_exec(code, allowed_classes=[Point, Circle], allow_dataclass_methods=True)
    assert abs(result - 78.54) < 0.01


def test_dataclass_attribute_access():
    @dataclass
    class Person:
        name: str
        age: int

    code = """
p = Person("Alice", 30)
p.name + " is " + str(p.age) + " years old"
"""
    result = safe_exec(code, allowed_classes=[Person])
    assert result == "Alice is 30 years old"