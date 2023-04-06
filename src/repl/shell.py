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
REPL shell for Visier SQL-like queries.
"""

from cmd import Cmd
from visier.connector import VisierSession, QueryExecutionError
from .cmd_queue import CommandQueue
from .constants import SQL_BYE, SQL_CONTINUE_PROMPT, SQL_OPTIONS, SQL_PROMPT
from .display import TableDisplay

class SqlLikeShell(Cmd):
    """REPL shell for Visier SQL-like queries"""
    def __init__(self, session: VisierSession, max_col_width: int):
        super().__init__()
        self.intro = """\x1b[1;32;40mWelcome to the Visier SQL-like Shell.
Type help or ? to list commands.

Don't forget to terminate each SQL-like statement with a semicolon (;)
\x1b[;;40m"""
        self.prompt = SQL_PROMPT
        self._command_queue = CommandQueue()
        self._session = session
        self._max_col_width = max_col_width
        self._transaction = None

    def default(self, line):
        "General shell command entry point"
        self._command_queue.ingest_line(line.strip())
        for cmd in self._command_queue.commands():
            self._execute(cmd)
        if self._command_queue.has_fragment():
            self.prompt = SQL_CONTINUE_PROMPT
        else:
            self.prompt = SQL_PROMPT

    def emptyline(self):
        "Empty line handler"
        pass

    def do_bye(self, _):
        "Exit the SQL-like shell"
        print(SQL_BYE)
        return True

    def _execute(self, cmd: str):
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
