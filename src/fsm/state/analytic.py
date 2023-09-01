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
Defines the FSM State for analytic SQL-like query execution.
"""

from typing import Tuple
from visier.connector import VisierSession, QueryExecutionError
from visier.api import QueryApiClient
from display.table import TableDisplay
from .state import State, is_set_cmd, parse_attr_cmd
from .constants import SQL_CONTINUE_PROMPT, SQL_PROMPT, SQL_OPTIONS, VALUE_STAGING, STATE_STAGING


class AnalyticState(State):
    """State for analytic SQL-like query execution."""
    def __init__(self, session: VisierSession, max_col_width: int) -> None:
        super().__init__()
        self._client = QueryApiClient(session, raise_on_error=True)
        self._max_col_width = max_col_width

    def prompt(self) -> str:
        return SQL_PROMPT

    def continue_prompt(self) -> str:
        return SQL_CONTINUE_PROMPT

    def execute(self, cmd: str) -> Tuple[str, object]:
        "Executes a SQL-like statement"
        if cmd[0:6].lower().startswith("select"):
            self._execute_data_query(cmd)
        elif is_set_cmd(cmd):
            try:
                # Will throw ValueError if cmd is not a valid SET statement,
                # setting the schema to staging
                parse_attr_cmd(cmd, VALUE_STAGING)
                return (STATE_STAGING, {})
            except ValueError as attr_set_error:
                self._error(attr_set_error)
        else:
            if len(cmd) > 1:
                self._error("Only SELECT or SET schema TO statements are supported")
            else:
                print("")
        return None

    def _execute_data_query(self, cmd: str):
        "Executes a data query"
        try:
            result = self._client.sqllike(cmd, SQL_OPTIONS)
            table = TableDisplay(result, max_col_width=self._max_col_width)
            table.display()
        except QueryExecutionError as error:
            self._error(f"Executing query {cmd}.\nDetails: {error}")
        except StopIteration:
            print("Query returned no results.")
