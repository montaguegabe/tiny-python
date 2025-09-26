from tiny_python import tiny_exec


def test_string_concatenation():
    code = """
text = "hello"
upper_text = text.upper()
result = upper_text + " WORLD"
result
"""
    assert tiny_exec(code) == "HELLO WORLD"


def test_string_split():
    code = """
words = "one,two,three"
split_words = words.split(",")
len(split_words)
"""
    assert tiny_exec(code) == 3


def test_string_join():
    code = """
words = ["hello", "world"]
" ".join(words)
"""
    assert tiny_exec(code) == "hello world"


def test_string_format():
    code = """
template = "Hello, {}!"
template.format("World")
"""
    assert tiny_exec(code) == "Hello, World!"


def test_string_methods():
    assert tiny_exec('"hello".upper()') == "HELLO"
    assert tiny_exec('"HELLO".lower()') == "hello"
    assert tiny_exec('"  hello  ".strip()') == "hello"
    assert tiny_exec('"hello world".replace("world", "python")') == "hello python"


def test_string_checks():
    assert tiny_exec('"123".isdigit()')
    assert tiny_exec('"abc".isalpha()')
    assert not tiny_exec('"123".isalpha()')
    assert tiny_exec('"abc123".isalnum()')


def test_string_search():
    assert tiny_exec('"hello world".find("world")') == 6
    assert tiny_exec('"hello world".find("xyz")') == -1
    assert tiny_exec('"hello world".startswith("hello")')
    assert tiny_exec('"hello world".endswith("world")')
