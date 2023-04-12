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
Defines the FSM State for analytic SQL-like query execution.
"""

from visier.connector import VisierSession, QueryExecutionError
from display.table import TableDisplay
from .state import State
from .constants import SQL_CONTINUE_PROMPT, SQL_PROMPT, SQL_OPTIONS


class AnalyticState(State):
    """State for analytic SQL-like query execution."""
    def __init__(self, session: VisierSession, max_col_width: int) -> None:
        super().__init__()
        self._session = session
        self._max_col_width = max_col_width

    def prompt(self) -> str:
        return SQL_PROMPT

    def continue_prompt(self) -> str:
        return SQL_CONTINUE_PROMPT

    def execute(self, cmd: str):
        "Executes a SQL-like statement"
        if len(cmd) > 6 and cmd[0:6].lower() == "select":
            self._execute_data_query(cmd)
        else:
            if len(cmd) > 1:
                self._error("Only SELECT statements are supported")
            else:
                print("")

    def _execute_data_query(self, cmd: str):
        "Executes a data query"
        try:
            result = self._session.execute_sqllike(cmd, SQL_OPTIONS)
            table = TableDisplay(result, max_col_width=self._max_col_width)
            table.display()
        except QueryExecutionError as error:
            self._error(f"Executing query {cmd}.\nDetails: {error}")
        except StopIteration:
            print("Query returned no results.")

    def _error(self, msg):
        "Prints an error message"
        print(f"\x1b[1;31;40mERROR: {msg}\x1b[0m")
