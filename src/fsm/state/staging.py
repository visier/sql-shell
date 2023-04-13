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
Defines the FSM State for staging SQL-like query execution.
"""

from typing import Tuple
from visier.connector import VisierSession
from .state import State, is_set_cmd, parse_attr_cmd
from .constants import (SQL_STAGING_PROMPT, SQL_STAGING_CONTINUE_PROMPT, 
                        VALUE_ANALYTIC, STATE_ANALYTIC)

class StagingState(State):
    """State for staging SQL-like query execution."""
    def __init__(self, session: VisierSession) -> None:
        super().__init__()
        self._session = session

    def prompt(self) -> str:
        return SQL_STAGING_PROMPT

    def continue_prompt(self) -> str:
        return SQL_STAGING_CONTINUE_PROMPT

    def execute(self, cmd: str) -> None | Tuple[str, object]:
        if is_set_cmd(cmd):
            try:
                # Will throw ValueError if cmd is not a valid SET statement,
                # setting the schema to analytic
                parse_attr_cmd(cmd, VALUE_ANALYTIC)
                return (STATE_ANALYTIC, {})
            except ValueError as attr_set_error:
                self._error(attr_set_error)
        return None
