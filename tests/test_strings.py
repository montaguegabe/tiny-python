from tiny_python import safe_exec


def test_string_concatenation():
    code = """
text = "hello"
upper_text = text.upper()
result = upper_text + " WORLD"
result
"""
    assert safe_exec(code) == "HELLO WORLD"


def test_string_split():
    code = """
words = "one,two,three"
split_words = words.split(",")
len(split_words)
"""
    assert safe_exec(code) == 3


def test_string_join():
    code = """
words = ["hello", "world"]
" ".join(words)
"""
    assert safe_exec(code) == "hello world"


def test_string_format():
    code = """
template = "Hello, {}!"
template.format("World")
"""
    assert safe_exec(code) == "Hello, World!"


def test_string_methods():
    assert safe_exec('"hello".upper()') == "HELLO"
    assert safe_exec('"HELLO".lower()') == "hello"
    assert safe_exec('"  hello  ".strip()') == "hello"
    assert safe_exec('"hello world".replace("world", "python")') == "hello python"


def test_string_checks():
    assert safe_exec('"123".isdigit()')
    assert safe_exec('"abc".isalpha()')
    assert not safe_exec('"123".isalpha()')
    assert safe_exec('"abc123".isalnum()')


def test_string_search():
    assert safe_exec('"hello world".find("world")') == 6
    assert safe_exec('"hello world".find("xyz")') == -1
    assert safe_exec('"hello world".startswith("hello")')
    assert safe_exec('"hello world".endswith("world")')