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

"""
Abstract representation of a state in the state machine
"""

import re
from abc import ABC
from typing import Tuple
from .constants import VALUE_ANALYTIC, VALUE_STAGING, ATTR_SCHEMA

class State(ABC):
    """
    Abstract representation of a state in the state machine
    """
    def __init__(self) -> None:
        super().__init__()
        self._params = {}

    def prompt(self) -> str:
        "Returns the prompt for the current state"

    def continue_prompt(self) -> str:
        "Returns the continuation prompt relevant for multi-line commands for the current state"

    def execute(self, cmd: str) -> Tuple[str, object]:
        "Executes a command in the current state"

    def put_parameters(self, params: object) -> None:
        "Sets the state's parameters"
        self._params = params

    def _error(self, msg):
        "Prints an error message"
        print(f"\x1b[1;31;40mERROR: {msg}\x1b[0m")


def is_set_cmd(cmd: str) -> bool:
    """
    Returns true if the command is a set command
    """
    return cmd.lower().startswith("set ")

def parse_attr_cmd(cmd: str, required_value: str = None) -> Tuple[str, str]:
    """
    Returns the attribute key value pair for recognized attribute commands
    """
    match_result = re.match(r"set\s+(?P<attr>\w+)\s+to\s+(?P<value>\w+)", cmd.lower())
    if not match_result:
        raise ValueError("Invalid attribute command.")
    if match_result.group("attr") != ATTR_SCHEMA:
        raise ValueError(f"Invalid attribute command. Only '{ATTR_SCHEMA}' is supported.")
    if not required_value and match_result.group("value") not in [VALUE_ANALYTIC, VALUE_STAGING]:
        raise ValueError(f"Invalid attribute command. Only '{VALUE_ANALYTIC}' and '{VALUE_STAGING}' are supported.")
    if required_value and match_result.group("value") != required_value:
        raise ValueError(f"Invalid attribute command. Only '{required_value}' is supported.")
    return (match_result.group("attr"), match_result.group("value"))
