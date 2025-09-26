from tiny_python import tiny_eval_last


def test_string_concatenation():
    code = """
text = "hello"
upper_text = text.upper()
result = upper_text + " WORLD"
result
"""
    assert tiny_eval_last(code) == "HELLO WORLD"


def test_string_split():
    code = """
words = "one,two,three"
split_words = words.split(",")
len(split_words)
"""
    assert tiny_eval_last(code) == 3


def test_string_join():
    code = """
words = ["hello", "world"]
" ".join(words)
"""
    assert tiny_eval_last(code) == "hello world"


def test_string_format():
    code = """
template = "Hello, {}!"
template.format("World")
"""
    assert tiny_eval_last(code) == "Hello, World!"


def test_string_methods():
    assert tiny_eval_last('"hello".upper()') == "HELLO"
    assert tiny_eval_last('"HELLO".lower()') == "hello"
    assert tiny_eval_last('"  hello  ".strip()') == "hello"
    assert tiny_eval_last('"hello world".replace("world", "python")') == "hello python"


def test_string_checks():
    assert tiny_eval_last('"123".isdigit()')
    assert tiny_eval_last('"abc".isalpha()')
    assert not tiny_eval_last('"123".isalpha()')
    assert tiny_eval_last('"abc123".isalnum()')


def test_string_search():
    assert tiny_eval_last('"hello world".find("world")') == 6
    assert tiny_eval_last('"hello world".find("xyz")') == -1
    assert tiny_eval_last('"hello world".startswith("hello")')
    assert tiny_eval_last('"hello world".endswith("world")')
