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
from visier.connector import VisierSession
from fsm import mk_fsm
from fsm.state.constants import SCHEMA_MAP
from .cmd_queue import CommandQueue
from .constants import SQL_INTRO, SQL_BYE


class SqlLikeShell(Cmd):
    """
    REPL shell for Visier SQL-like queries
    """
    def __init__(self, session: VisierSession,
                 max_col_width: int,
                 initial_schema: str):
        super().__init__()
        self.intro = SQL_INTRO
        self._fsm = mk_fsm(session, max_col_width, SCHEMA_MAP[initial_schema])
        self.prompt = self._fsm.prompt()
        self._command_queue = CommandQueue()
        self._transaction = None

    def default(self, line):
        """
        General shell command entry point
        """
        self._command_queue.ingest_line(line.strip())
        for cmd in self._command_queue.commands():
            self._fsm.execute(cmd)
        if self._command_queue.has_fragment():
            self.prompt = self._fsm.continue_prompt()
        else:
            self.prompt = self._fsm.prompt()

    def emptyline(self):
        """
        Empty line handler
        """

    def do_bye(self, _):
        """
        Exit the SQL-like shell
        """
        print(SQL_BYE)
        return True
