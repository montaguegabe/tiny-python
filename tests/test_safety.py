import pytest

from tiny_python import tiny_eval_last
from tiny_python.executor import ExecutionError


def test_import_blocked():
    with pytest.raises(ValueError):
        tiny_eval_last("import os")

    with pytest.raises(ValueError):
        tiny_eval_last("from os import path")


def test_exec_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("exec('print(1)')")


def test_eval_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("eval('1+1')")


def test_open_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("open('file.txt')")


def test_compile_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("compile('1+1', 'string', 'eval')")


def test_dunder_access_blocked():
    with pytest.raises(ValueError):
        tiny_eval_last("__import__('os')")

    with pytest.raises(ValueError):
        tiny_eval_last("__builtins__")

    with pytest.raises(ValueError):
        tiny_eval_last("__file__")


def test_globals_locals_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("globals()")

    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("locals()")

    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("vars()")


def test_attribute_access_blocked():
    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("getattr(str, '__class__')")

    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("setattr(str, 'test', 123)")

    with pytest.raises((ValueError, NameError)):
        tiny_eval_last("delattr(str, 'test')")


def test_max_iterations():
    with pytest.raises(ExecutionError, match="iterations"):
        tiny_eval_last(
            """
while True:
    pass
""",
            max_iterations=100,
        )

    with pytest.raises(ExecutionError, match="iterations"):
        tiny_eval_last(
            """
for i in range(1000000):
    x = i * 2
""",
            max_iterations=100,
        )


def test_iteration_limit_not_triggered():
    # This should work fine
    code = """
total = 0
for i in range(10):
    total += i
total
"""
    result = tiny_eval_last(code, max_iterations=100)
    assert result == 45


def test_function_definition_blocked():
    with pytest.raises(ValueError):
        tiny_eval_last("""
def my_func():
    return 42
""")

    with pytest.raises(ValueError):
        tiny_eval_last("""
lambda x: x * 2
""")


def test_max_iterations_per_loop():
    """Test that max_iterations_per_loop limits individual loop iterations."""

    # Test with for loop exceeding limit
    with pytest.raises(ExecutionError, match="Exceeded maximum iterations per loop"):
        tiny_eval_last(
            """
total = 0
for i in range(1000):
    total += i
total
""",
            max_iterations_per_loop=100,
        )

    # Test with while loop exceeding limit
    with pytest.raises(ExecutionError, match="Exceeded maximum iterations per loop"):
        tiny_eval_last(
            """
i = 0
while i < 1000:
    i += 1
i
""",
            max_iterations_per_loop=100,
        )

    # Test that loops within limit work fine
    result = tiny_eval_last(
        """
total = 0
for i in range(50):
    total += i
total
""",
        max_iterations_per_loop=100,
    )
    assert result == sum(range(50))

    # Test nested loops - each loop has its own counter
    result = tiny_eval_last(
        """
total = 0
for i in range(10):
    for j in range(10):
        total += 1
total
""",
        max_iterations_per_loop=15,  # Each loop runs 10 times, which is under 15
    )
    assert result == 100

    # Test that break statement works and doesn't trigger limit
    result = tiny_eval_last(
        """
i = 0
while True:
    i += 1
    if i == 5:
        break
i
""",
        max_iterations_per_loop=10,
    )
    assert result == 5


def test_max_iterations_vs_max_iterations_per_loop():
    """Test interaction between max_iterations and max_iterations_per_loop."""

    # max_iterations_per_loop should trigger first if lower
    with pytest.raises(ExecutionError, match="Exceeded maximum iterations per loop"):
        tiny_eval_last(
            """
for i in range(50):
    pass
""",
            max_iterations=1000,
            max_iterations_per_loop=40,
        )

    # max_iterations should trigger for total operations across multiple loops
    with pytest.raises(ExecutionError, match="Exceeded maximum iterations"):
        tiny_eval_last(
            """
# Each loop is under per-loop limit but total exceeds max_iterations
for i in range(30):
    pass
for j in range(30):
    pass
for k in range(30):
    pass
""",
            max_iterations=50,  # Total will be 90 iterations
            max_iterations_per_loop=40,  # Each loop is under this
        )

    # Nested loops where inner iterations count toward total
    with pytest.raises(ExecutionError, match="Exceeded maximum iterations"):
        tiny_eval_last(
            """
for i in range(10):
    for j in range(10):
        x = i + j  # 100 total iterations
""",
            max_iterations=50,
            max_iterations_per_loop=20,
        )
