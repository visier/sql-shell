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
REPL shell for Visier SQL-like queries.
"""

from cmd import Cmd
from visier.connector import VisierSession
from fsm import mk_fsm
from fsm.state.constants import SCHEMA_MAP
from .cmd_queue import CommandQueue
from .constants import SQL_INTRO, SQL_EXIT


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

    def emptyline(self) -> bool:
        """Empty line handler. Do nothing."""

    def do_bye(self, _):
        """
        Exit the SQL-like shell
        """
        return self._exit()

    def do_exit(self, _):
        """
        Exit the SQL-like shell
        """
        return self._exit()

    def do_quit(self, _):
        """
        Exit the SQL-like shell
        """
        return self._exit()

    def _exit(self):
        """
        Exit the SQL-like shell
        """
        print(SQL_EXIT)
        return True
