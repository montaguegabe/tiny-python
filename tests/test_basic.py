from dataclasses import dataclass

import pytest

from tiny_python import Executor, tiny_exec
from tiny_python.executor import ExecutionError


class TestMathOperations:
    def test_addition(self):
        assert tiny_exec("2 + 3") == 5

    def test_subtraction(self):
        assert tiny_exec("10 - 4") == 6

    def test_multiplication(self):
        assert tiny_exec("3 * 4") == 12

    def test_division(self):
        assert tiny_exec("15 / 3") == 5.0

    def test_floor_division(self):
        assert tiny_exec("17 // 5") == 3

    def test_modulo(self):
        assert tiny_exec("17 % 5") == 2

    def test_power(self):
        assert tiny_exec("2 ** 3") == 8

    def test_complex_expression(self):
        assert tiny_exec("2 + 3 * 4 - 1") == 13


class TestVariables:
    def test_simple_assignment(self):
        code = """
x = 10
x
"""
        assert tiny_exec(code) == 10

    def test_multiple_assignments(self):
        code = """
x = 10
y = 20
z = x + y
z
"""
        assert tiny_exec(code) == 30

    def test_augmented_assignment(self):
        code = """
x = 10
x += 5
x *= 2
x
"""
        assert tiny_exec(code) == 30


class TestStringOperations:
    def test_string_methods(self):
        code = """
text = "hello"
upper_text = text.upper()
result = upper_text + " WORLD"
result
"""
        assert tiny_exec(code) == "HELLO WORLD"

    def test_string_split(self):
        code = """
words = "one,two,three"
split_words = words.split(",")
len(split_words)
"""
        assert tiny_exec(code) == 3

    def test_string_join(self):
        code = """
words = ["hello", "world"]
" ".join(words)
"""
        assert tiny_exec(code) == "hello world"

    def test_string_format(self):
        code = """
template = "Hello, {}!"
template.format("World")
"""
        assert tiny_exec(code) == "Hello, World!"


class TestCollections:
    def test_list_operations(self):
        code = """
numbers = [1, 2, 3]
numbers.append(4)
numbers.extend([5, 6])
sum(numbers)
"""
        assert tiny_exec(code) == 21

    def test_list_comprehension_alternative(self):
        code = """
items = []
for i in range(5):
    items.append(i * 2)
items
"""
        assert tiny_exec(code) == [0, 2, 4, 6, 8]

    def test_dictionary_operations(self):
        code = """
data = {"a": 1, "b": 2}
data["c"] = 3
data.get("d", 10)
"""
        assert tiny_exec(code) == 10

    def test_dictionary_iteration(self):
        code = """
scores = {}
for i in range(3):
    scores[str(i)] = i * 10
sum(scores.values())
"""
        assert tiny_exec(code) == 30

    def test_tuple_operations(self):
        code = """
t = (1, 2, 3)
a, b, c = t
a + b + c
"""
        assert tiny_exec(code) == 6


class TestControlFlow:
    def test_if_statement(self):
        code = """
x = 10
if x > 5:
    result = "greater"
else:
    result = "lesser"
result
"""
        assert tiny_exec(code) == "greater"

    def test_elif_statement(self):
        code = """
x = 5
if x > 10:
    result = "high"
elif x > 3:
    result = "medium"
else:
    result = "low"
result
"""
        assert tiny_exec(code) == "medium"

    def test_for_loop(self):
        code = """
total = 0
for i in range(5):
    total += i
total
"""
        assert tiny_exec(code) == 10

    def test_while_loop(self):
        code = """
count = 0
value = 1
while value < 100:
    value = value * 2
    count += 1
count
"""
        assert tiny_exec(code) == 7

    def test_break_continue(self):
        code = """
result = []
for i in range(10):
    if i == 5:
        break
    if i % 2 == 1:
        continue
    result.append(i)
result
"""
        assert tiny_exec(code) == [0, 2, 4]

    def test_nested_loops(self):
        code = """
total = 0
for i in range(3):
    for j in range(3):
        total += i * j
total
"""
        assert tiny_exec(code) == 9


class TestDataclasses:
    def test_dataclass_instantiation(self):
        @dataclass
        class Point:
            x: float
            y: float

        code = """
p = Point(3, 4)
p.x + p.y
"""
        result = tiny_exec(code, allowed_classes=[Point])
        assert result == 7

    def test_dataclass_with_kwargs(self):
        @dataclass
        class Point:
            x: float
            y: float

        code = """
p = Point(x=5, y=12)
(p.x ** 2 + p.y ** 2) ** 0.5
"""
        result = tiny_exec(code, allowed_classes=[Point])
        assert abs(result - 13.0) < 0.01

    def test_dataclass_with_methods(self):
        @dataclass
        class Rectangle:
            width: float
            height: float

            def area(self):
                return self.width * self.height

        code = """
rect = Rectangle(10, 20)
rect.area()
"""
        assert tiny_exec(code, allowed_classes=[Rectangle]) == 200


class TestBuiltinFunctions:
    def test_len(self):
        assert tiny_exec("len([1, 2, 3, 4, 5])") == 5

    def test_range(self):
        code = """
list(range(5))
"""
        assert tiny_exec(code) == [0, 1, 2, 3, 4]

    def test_type_conversions(self):
        assert tiny_exec("int('42')") == 42
        assert tiny_exec("float('3.14')") == 3.14
        assert tiny_exec("str(123)") == "123"
        assert tiny_exec("bool(1)") == True

    def test_min_max(self):
        assert tiny_exec("min([3, 1, 4, 1, 5])") == 1
        assert tiny_exec("max([3, 1, 4, 1, 5])") == 5

    def test_sum(self):
        assert tiny_exec("sum([1, 2, 3, 4, 5])") == 15

    def test_sorted(self):
        assert tiny_exec("sorted([3, 1, 4, 1, 5])") == [1, 1, 3, 4, 5]

    def test_enumerate(self):
        code = """
result = []
for i, val in enumerate(['a', 'b', 'c']):
    result.append((i, val))
result
"""
        assert tiny_exec(code) == [(0, "a"), (1, "b"), (2, "c")]


class TestGlobalVariables:
    def test_global_vars_access(self):
        code = """
result = pi * radius ** 2
result
"""
        result = tiny_exec(code, global_vars={"pi": 3.14159, "radius": 5})
        assert abs(result - 78.54) < 0.01

    def test_global_vars_with_locals(self):
        code = """
local_var = 10
result = local_var + global_var
result
"""
        assert tiny_exec(code, global_vars={"global_var": 20}) == 30


class TestSafetyFeatures:
    def test_import_blocked(self):
        with pytest.raises(SyntaxError):
            tiny_exec("import os")

    def test_exec_blocked(self):
        with pytest.raises((ValueError, NameError)):
            tiny_exec("exec('print(1)')")

    def test_eval_blocked(self):
        with pytest.raises((ValueError, NameError)):
            tiny_exec("eval('1+1')")

    def test_open_blocked(self):
        with pytest.raises((ValueError, NameError)):
            tiny_exec("open('file.txt')")

    def test_dunder_access_blocked(self):
        with pytest.raises(ValueError):
            tiny_exec("__import__('os')")

    def test_max_iterations(self):
        with pytest.raises(ExecutionError, match="iterations"):
            tiny_exec(
                """
while True:
    pass
""",
                max_iterations=100,
            )

    def test_max_recursion(self):
        # This would need a recursive function, which we don't support directly
        # but we can test the limit exists
        executor = Executor(max_recursion_depth=5)
        assert executor.max_recursion_depth == 5


class TestExecutorClass:
    def test_executor_initialization(self):
        executor = Executor(max_iterations=1000)
        assert executor.max_iterations == 1000

    def test_multiple_executions(self):
        executor = Executor()

        result1 = executor.execute("x = 10; x * 2")
        assert result1 == 20

        # Each execution starts fresh
        result2 = executor.execute("y = 5; y + 3")
        assert result2 == 8

    def test_executor_with_allowed_classes(self):
        @dataclass
        class TestClass:
            value: int

        executor = Executor(allowed_classes=[TestClass])
        result = executor.execute("obj = TestClass(42); obj.value")
        assert result == 42


class TestEdgeCases:
    def test_empty_code(self):
        assert tiny_exec("") is None

    def test_pass_statement(self):
        assert tiny_exec("pass") is None

    def test_multiple_statements_return_last(self):
        code = """
a = 1
b = 2
c = 3
a + b + c
"""
        assert tiny_exec(code) == 6

    def test_comparison_operators(self):
        assert tiny_exec("5 > 3") == True
        assert tiny_exec("5 < 3") == False
        assert tiny_exec("5 == 5") == True
        assert tiny_exec("5 != 3") == True
        assert tiny_exec("5 >= 5") == True
        assert tiny_exec("3 <= 5") == True

    def test_boolean_operators(self):
        assert tiny_exec("True and False") == False
        assert tiny_exec("True or False") == True
        assert tiny_exec("not True") == False

    def test_in_operator(self):
        assert tiny_exec("3 in [1, 2, 3, 4]") == True
        assert tiny_exec("5 not in [1, 2, 3, 4]") == True
