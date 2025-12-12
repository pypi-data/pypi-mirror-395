from zyng.runner import parse_line_to_statement
from zyng.core import Show, Let


def test_parse_show_with_time_now():
    stmt = parse_line_to_statement('show "Hello" :::now')
    assert isinstance(stmt, Show)
    assert stmt.content == "Hello"
    assert stmt.time == "now"


def test_parse_let_simple():
    stmt = parse_line_to_statement('let user = "Alice"')
    assert isinstance(stmt, Let)
    assert stmt.name == "user"
    assert stmt.value == "Alice"
