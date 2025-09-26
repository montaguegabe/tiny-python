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


def test_dataclass_attribute_setting():
    """Test setting attributes on a dataclass."""
    @dataclass
    class Person:
        name: str
        age: int

    code = """
p = Person("Bob", 25)
p.age = 26
p.name = "Robert"
[p.name, p.age]
"""
    result = tiny_eval_last(code, allowed_classes=[Person])
    assert result == ["Robert", 26]


def test_dataclass_conversion_in_locals():
    """Test that SafeDataClass instances are converted to real dataclasses in returned locals."""
    from tiny_python import tiny_exec

    @dataclass
    class Point:
        x: float
        y: float

    code = """
p1 = Point(1.0, 2.0)
p2 = Point(3.0, 4.0)
distance = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
"""
    locals_dict = tiny_exec(code, allowed_classes=[Point])

    # Check that p1 and p2 are real Point instances, not SafeDataClass
    assert isinstance(locals_dict["p1"], Point)
    assert isinstance(locals_dict["p2"], Point)
    assert locals_dict["p1"].x == 1.0
    assert locals_dict["p1"].y == 2.0
    assert locals_dict["p2"].x == 3.0
    assert locals_dict["p2"].y == 4.0
    assert abs(locals_dict["distance"] - 2.828) < 0.01


def test_dataclass_in_last_result():
    """Test that SafeDataClass is converted to real dataclass when it's the last result."""
    @dataclass
    class Person:
        name: str
        age: int

    code = """
Person("Charlie", 35)
"""
    result = tiny_eval_last(code, allowed_classes=[Person])

    # Check that result is a real Person instance
    assert isinstance(result, Person)
    assert result.name == "Charlie"
    assert result.age == 35


def test_nested_dataclasses():
    """Test that nested dataclasses are properly converted."""
    from tiny_python import tiny_exec

    @dataclass
    class Address:
        street: str
        city: str

    @dataclass
    class Person:
        name: str
        address: Address

    code = """
addr = Address("123 Main St", "NYC")
person = Person("David", addr)
"""
    locals_dict = tiny_exec(code, allowed_classes=[Person, Address])

    # Check that both dataclasses are real instances
    assert isinstance(locals_dict["addr"], Address)
    assert isinstance(locals_dict["person"], Person)
    assert isinstance(locals_dict["person"].address, Address)
    assert locals_dict["person"].address.city == "NYC"


def test_dataclass_in_list():
    """Test that dataclasses in lists are converted."""
    from tiny_python import tiny_exec

    @dataclass
    class Item:
        name: str
        value: int

    code = """
items = [Item("apple", 10), Item("banana", 5), Item("cherry", 15)]
values = []
for item in items:
    values = values + [item.value]
total = sum(values)
"""
    locals_dict = tiny_exec(code, allowed_classes=[Item])

    # Check that all items in the list are real Item instances
    assert len(locals_dict["items"]) == 3
    for item in locals_dict["items"]:
        assert isinstance(item, Item)
    assert locals_dict["items"][0].name == "apple"
    assert locals_dict["total"] == 30
