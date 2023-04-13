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
Test cases for the attribute command parser
"""

import pytest
from fsm.state import parse_attr_cmd


INVALID_ATTR_CMD = "Invalid attribute command."

# test cases for various attribute commands
def test_should_handle_empty_command():
    with pytest.raises(ValueError, match=INVALID_ATTR_CMD):
        parse_attr_cmd("")

def test_should_handle_invalid_command():
    with pytest.raises(ValueError, match=INVALID_ATTR_CMD):
        parse_attr_cmd("foo")

def test_should_handle_set_invalid_attribute():
    with pytest.raises(ValueError, match=f"{INVALID_ATTR_CMD} Only 'schema' is supported."):
        parse_attr_cmd("set foo to something")

def test_should_handle_set_invalid_value():
    with pytest.raises(ValueError,
                       match=f"{INVALID_ATTR_CMD} Only 'analytic' and 'staging' are supported."):
        parse_attr_cmd("set schema to something")

def test_should_handle_set_analytic_schema():
    assert parse_attr_cmd("set schema to analytic") == ("schema", "analytic")

def test_should_handle_set_staging_schema():
    assert parse_attr_cmd("set schema to staging") == ("schema", "staging")

def test_should_handle_valid_set_command_with_random_spaces():
    assert parse_attr_cmd("set  schema to analytic") == ("schema", "analytic")
    assert parse_attr_cmd("set schema  to analytic ") == ("schema", "analytic")
    assert parse_attr_cmd("set schema to  analytic") == ("schema", "analytic")
    assert parse_attr_cmd("set     schema    to     analytic ") == ("schema", "analytic")

def test_should_handle_valid_set_command_with_random_case():
    assert parse_attr_cmd("set SCHEMA to analytic") == ("schema", "analytic")
    assert parse_attr_cmd("set schema TO analytic") == ("schema", "analytic")
    assert parse_attr_cmd("set schema to ANALYTIC") == ("schema", "analytic")
    assert parse_attr_cmd("set SCHEMA TO ANALYTIC") == ("schema", "analytic")

def test_should_handle_set_command_with_value_that_does_not_match_required_value():
    with pytest.raises(ValueError, match=f"{INVALID_ATTR_CMD} Only 'analytic' is supported."):
        parse_attr_cmd("set schema to staging", "analytic")
    with pytest.raises(ValueError, match=f"{INVALID_ATTR_CMD} Only 'staging' is supported."):
        parse_attr_cmd("set schema to analytic", "staging")

def test_should_handle_set_command_with_value_that_matches_required_value():
    assert parse_attr_cmd("set schema to analytic", "analytic") == ("schema", "analytic")
    assert parse_attr_cmd("set schema to staging", "staging") == ("schema", "staging")

if __name__ == "__main__":
    pytest.main()
