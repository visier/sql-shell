# Copyright 2023 Visier Solutions Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=missing-function-docstring

"""
Test cases for the command queue
"""

import pytest
from repl import CommandQueue as CmdQueue


# test cases for various line inputs that are both complete commands and fragments
def test_should_handle_complete_commands():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo;")
    queue.ingest_line("SELECT * FROM bar;")
    assert list(queue.commands()) == ["SELECT * FROM foo", "SELECT * FROM bar"]
    assert not queue.has_fragment()

def test_should_handle_complete_commands_with_semicolons_in_string_literals():
    queue = CmdQueue()
    queue.ingest_line("SELECT * FROM foo WHERE bar = 'foo;bar'; SELECT * FROM bar;")
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
