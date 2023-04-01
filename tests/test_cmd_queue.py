import pytest
from src.repl import CommandQueue as CmdQueue

# test cases for various line inputs that are both complete commands and fragments
def test_should_handle_complete_commands():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo;")
    queue.ingest_line("SELECT * FROM bar;")
    assert [x for x in queue.commands()] == ["SELECT * FROM foo", "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_handle_complete_commands_with_semicolons_in_string_literals():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo WHERE bar = 'foo;bar';SELECT * FROM bar;")
    assert [x for x in queue.commands()] == ["SELECT * FROM foo WHERE bar = 'foo;bar'", "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_handle_command_composition_with_multiple_fragment_lines():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo")
    queue.ingest_line("WHERE bar = 'foo';SELECT * FROM bar;")
    assert [x for x in queue.commands()] == ["SELECT * FROM foo\nWHERE bar = 'foo'", "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_not_add_final_fragment_to_complete_command():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo;")
    queue.ingest_line("SELECT * FROM bar")
    queue.ingest_line("WHERE baz = 'bar'; SELECT * FROM baz")
    assert [x for x in queue.commands()] == ["SELECT * FROM foo", "SELECT * FROM bar\nWHERE baz = 'bar'"]
    assert queue.has_fragment()
    assert queue._fragment == "SELECT * FROM baz"

if __name__ == "__main__":
    pytest.main()