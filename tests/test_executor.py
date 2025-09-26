from dataclasses import dataclass

from tiny_python import Executor, tiny_exec


def test_executor_initialization():
    executor = Executor(max_iterations=1000)
    assert executor.max_iterations == 1000


def test_multiple_executions():
    executor = Executor()

    result1 = executor.execute("x = 10; x * 2")
    assert result1 == 20

    # Each execution starts fresh
    result2 = executor.execute("y = 5; y + 3")
    assert result2 == 8


def test_executor_with_allowed_classes():
    @dataclass
    class TestClass:
        value: int

    executor = Executor(allowed_classes=[TestClass])
    result = executor.execute("obj = TestClass(42); obj.value")
    assert result == 42


def test_executor_with_global_vars():
    executor = Executor(global_vars={"pi": 3.14159, "e": 2.71828})
    result = executor.execute("pi + e")
    assert abs(result - 5.85987) < 0.00001


def test_executor_limits():
    executor = Executor(max_iterations=5)

    # This should fail
    try:
        executor.execute("""
for i in range(10):
    x = i
""")
        assert False, "Should have raised ExecutionError"
    except Exception as e:
        assert "iterations" in str(e)


def test_tiny_exec_vs_executor():
    # Both should give same results
    code = "2 + 3 * 4"

    result1 = tiny_exec(code)
    executor = Executor()
    result2 = executor.execute(code)

    assert result1 == result2 == 14
