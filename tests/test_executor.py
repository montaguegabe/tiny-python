from dataclasses import dataclass

from tiny_python import Executor, tiny_eval_last


def test_executor_initialization():
    executor = Executor(max_iterations=1000)
    assert executor.max_iterations == 1000


def test_multiple_executions():
    executor = Executor()

    locals1 = executor.execute("x = 10; x * 2")
    assert executor.last_result == 20
    assert locals1["x"] == 10

    # Each execution starts fresh
    locals2 = executor.execute("y = 5; y + 3")
    assert executor.last_result == 8
    assert locals2["y"] == 5
    assert "x" not in locals2  # Previous execution's variables don't persist


def test_executor_with_allowed_classes():
    @dataclass
    class TestClass:
        value: int

    executor = Executor(allowed_classes=[TestClass])
    locals_dict = executor.execute("obj = TestClass(42); obj.value")
    assert executor.last_result == 42
    assert "obj" in locals_dict  # obj should be in locals


def test_executor_with_global_vars():
    executor = Executor(global_vars={"pi": 3.14159, "e": 2.71828})
    locals_dict = executor.execute("pi + e")
    assert abs(executor.last_result - 5.85987) < 0.00001


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


def test_tiny_eval_last_vs_executor():
    # Both should give same last result
    code = "2 + 3 * 4"

    result1 = tiny_eval_last(code)

    executor = Executor()
    executor.execute(code)
    result2 = executor.last_result

    assert result1 == result2 == 14
