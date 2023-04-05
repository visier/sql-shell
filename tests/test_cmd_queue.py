# This file is part of visier-sqllike-shell.
#
# visier-sqllike-shell is free software: you can redistribute it and/or modify
# it under the terms of the Apache License, Version 2.0 (the "License").
#
# visier-sqllike-shell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License, Version 2.0 for more details.
#
# You should have received a copy of the Apache License, Version 2.0
# along with visier-sqllike-shell. If not, see <https://www.apache.org/licenses/LICENSE-2.0>.
# pylint: disable=missing-function-docstring

"""
Test cases for the command queue
"""

import pytest
from src.repl import CommandQueue as CmdQueue


# test cases for various line inputs that are both complete commands and fragments
def test_should_handle_complete_commands():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo;")
    queue.ingest_line("SELECT * FROM bar;")
    assert list(queue.commands()) == ["SELECT * FROM foo", "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_handle_complete_commands_with_semicolons_in_string_literals():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo WHERE bar = 'foo;bar';SELECT * FROM bar;")
    assert list(queue.commands()) == ["SELECT * FROM foo WHERE bar = 'foo;bar'",
                                      "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_handle_command_composition_with_multiple_fragment_lines():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo")
    queue.ingest_line("WHERE bar = 'foo';SELECT * FROM bar;")
    assert list(queue.commands()) == ["SELECT * FROM foo\nWHERE bar = 'foo'",
                                      "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_not_add_final_fragment_to_complete_command():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo;")
    queue.ingest_line("SELECT * FROM bar")
    queue.ingest_line("WHERE baz = 'bar'; SELECT * FROM baz")
    assert list(queue.commands()) == ["SELECT * FROM foo",
                                      "SELECT * FROM bar\nWHERE baz = 'bar'"]
    assert queue.has_fragment()
    assert queue.fragment() == "SELECT * FROM baz"

if __name__ == "__main__":
    pytest.main()
