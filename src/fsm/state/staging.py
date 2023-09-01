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
Defines the FSM State for staging SQL-like query execution.
"""

import re
from typing import Tuple
from visier.connector import VisierSession, QueryExecutionError
from visier.api import DirectIntakeApiClient
from .state import State, is_set_cmd, parse_attr_cmd
from .constants import (SQL_STAGING_PROMPT,
                        SQL_STAGING_CONTINUE_PROMPT,
                        VALUE_ANALYTIC,
                        STATE_ANALYTIC,
                        STATE_TRANSACTION)

class StagingState(State):
    """State for staging SQL-like query execution."""
    def __init__(self, session: VisierSession) -> None:
        super().__init__()
        self._begin = re.compile(r'^\s*begin\s+transaction\s*$', re.IGNORECASE)
        self._client = DirectIntakeApiClient(session, raise_on_error=True)

    def prompt(self) -> str:
        return SQL_STAGING_PROMPT

    def continue_prompt(self) -> str:
        return SQL_STAGING_CONTINUE_PROMPT

    def execute(self, cmd: str) -> Tuple[str, object]:
        if is_set_cmd(cmd):
            try:
                # Will throw ValueError if cmd is not a valid SET statement,
                # setting the schema to analytic
                parse_attr_cmd(cmd, VALUE_ANALYTIC)
                return (STATE_ANALYTIC, {})
            except ValueError as attr_set_error:
                self._error(attr_set_error)
        elif self._is_begin_cmd(cmd):
            return self._execute_begin()
        else:
            self._error(f"Invalid command: {cmd}")
        return None

    def _is_begin_cmd(self, cmd: str) -> bool:
        return self._begin.match(cmd) is not None

    def _execute_begin(self) -> Tuple[str, object]:
        try:
            response = self._client.start_transaction()
            return (STATE_TRANSACTION, response.json())
        except QueryExecutionError as query_exec_error:
            self._error(f"Failed to start transaction: {query_exec_error}")
            return None
