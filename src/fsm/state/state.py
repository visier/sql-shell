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

"""
Abstract representation of a state in the state machine
"""

import re
from abc import ABC
from typing import Tuple
from .constants import VALUE_ANALYTIC, VALUE_STAGING, ATTR_SCHEMA

class State(ABC):
    "Abstract base class for a state in the state machine"
    def prompt(self) -> str:
        "Returns the prompt for the current state"

    def continue_prompt(self) -> str:
        "Returns the continuation prompt relevant for multi-line commands for the current state"

    def execute(self, cmd: str) -> None | Tuple[str, object]:
        "Executes a command in the current state"

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
