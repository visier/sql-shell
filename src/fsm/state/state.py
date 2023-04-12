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

from abc import ABC


class State(ABC):
    "Abstract base class for a state in the state machine"
    def prompt(self) -> str:
        "Returns the prompt for the current state"

    def continue_prompt(self) -> str:
        "Returns the continuation prompt relevant for multi-line commands for the current state"

    def execute(self, cmd: str):
        "Executes a command in the current state"
