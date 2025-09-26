from tiny_python import tiny_exec


def test_global_vars_access():
    code = """
result = pi * radius ** 2
result
"""
    result = tiny_exec(code, global_vars={"pi": 3.14159, "radius": 5})
    assert abs(result - 78.54) < 0.01


def test_global_vars_with_locals():
    code = """
local_var = 10
result = local_var + global_var
result
"""
    assert tiny_exec(code, global_vars={"global_var": 20}) == 30


def test_global_override():
    code = """
x = 100
x
"""
    # Global x should not override local assignment
    result = tiny_exec(code, global_vars={"x": 50})
    assert result == 100


def test_global_functions():
    def custom_func(x):
        return x * 2

    code = """
result = custom_func(5)
result
"""
    assert (
        tiny_exec(code, global_vars={"custom_func": custom_func}, allow_global_functions=True) == 10
    )


def test_global_constants():
    code = """
area = WIDTH * HEIGHT
area
"""
    result = tiny_exec(code, global_vars={"WIDTH": 10, "HEIGHT": 20})
    assert result == 200


def test_mixed_globals():
    import math

    code = """
result = sqrt(x ** 2 + y ** 2)
int(result)
"""
    result = tiny_exec(
        code, global_vars={"sqrt": math.sqrt, "x": 3, "y": 4}, allow_global_functions=True
    )
    assert result == 5
