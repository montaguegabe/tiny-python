from tiny_python import tiny_eval_last


def test_list_creation():
    assert tiny_eval_last("[1, 2, 3]") == [1, 2, 3]
    assert tiny_eval_last("[]") == []


def test_list_append():
    code = """
numbers = [1, 2, 3]
numbers.append(4)
numbers
"""
    assert tiny_eval_last(code) == [1, 2, 3, 4]


def test_list_extend():
    code = """
numbers = [1, 2, 3]
numbers.extend([4, 5, 6])
numbers
"""
    assert tiny_eval_last(code) == [1, 2, 3, 4, 5, 6]


def test_list_operations():
    code = """
numbers = [1, 2, 3]
numbers.append(4)
numbers.extend([5, 6])
sum(numbers)
"""
    assert tiny_eval_last(code) == 21


def test_list_indexing():
    code = """
items = [10, 20, 30, 40]
items[0] + items[-1]
"""
    assert tiny_eval_last(code) == 50


def test_list_slicing():
    code = """
items = [1, 2, 3, 4, 5]
items[1:4]
"""
    assert tiny_eval_last(code) == [2, 3, 4]


def test_dictionary_creation():
    assert tiny_eval_last('{"a": 1, "b": 2}') == {"a": 1, "b": 2}
    assert tiny_eval_last("{}") == {}


def test_dictionary_operations():
    code = """
data = {"a": 1, "b": 2}
data["c"] = 3
data.get("d", 10)
"""
    assert tiny_eval_last(code) == 10


def test_dictionary_methods():
    code = """
data = {"a": 1, "b": 2}
list(data.keys())
"""
    assert tiny_eval_last(code) == ["a", "b"]

    code = """
data = {"a": 1, "b": 2}
list(data.values())
"""
    assert tiny_eval_last(code) == [1, 2]


def test_tuple_creation():
    assert tiny_eval_last("(1, 2, 3)") == (1, 2, 3)
    assert tiny_eval_last("()") == ()


def test_set_creation():
    code = """
s = set([1, 2, 2, 3])
len(s)
"""
    assert tiny_eval_last(code) == 3
