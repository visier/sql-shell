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
