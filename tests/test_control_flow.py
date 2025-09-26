from tiny_python import tiny_eval_last


def test_if_statement():
    code = """
x = 10
if x > 5:
    result = "greater"
else:
    result = "lesser"
result
"""
    assert tiny_eval_last(code) == "greater"


def test_elif_statement():
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
    assert tiny_eval_last(code) == "medium"


def test_nested_if():
    code = """
x = 10
y = 5
if x > 5:
    if y < 10:
        result = "both"
    else:
        result = "x only"
else:
    result = "neither"
result
"""
    assert tiny_eval_last(code) == "both"


def test_for_loop():
    code = """
total = 0
for i in range(5):
    total += i
total
"""
    assert tiny_eval_last(code) == 10


def test_for_loop_with_list():
    code = """
items = []
for i in range(5):
    items.append(i * 2)
items
"""
    assert tiny_eval_last(code) == [0, 2, 4, 6, 8]


def test_while_loop():
    code = """
count = 0
value = 1
while value < 100:
    value = value * 2
    count += 1
count
"""
    assert tiny_eval_last(code) == 7


def test_break_statement():
    code = """
result = []
for i in range(10):
    if i == 5:
        break
    result.append(i)
result
"""
    assert tiny_eval_last(code) == [0, 1, 2, 3, 4]


def test_continue_statement():
    code = """
result = []
for i in range(5):
    if i % 2 == 1:
        continue
    result.append(i)
result
"""
    assert tiny_eval_last(code) == [0, 2, 4]


def test_break_and_continue():
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
    assert tiny_eval_last(code) == [0, 2, 4]


def test_nested_loops():
    code = """
total = 0
for i in range(3):
    for j in range(3):
        total += i * j
total
"""
    assert tiny_eval_last(code) == 9


def test_for_else():
    code = """
for i in range(3):
    if i == 5:
        break
else:
    result = "completed"
result
"""
    assert tiny_eval_last(code) == "completed"
