from cmd import Cmd
from visier.connector import VisierSession
from .cmd_queue import CommandQueue
from .constants import *
from .display import TableDisplay


class SqlLikeShell(Cmd):
    """REPL shell for Visier SQL-like queries"""
    def __init__(self, session: VisierSession, max_col_width: int): 
        super().__init__()
        self.intro = """\x1b[1;32;40mWelcome to the Visier SQL-like Shell.
Type help or ? to list commands.

Don't forget to terminate each SQL-like statement with a semicolon (;)
\x1b[0m"""
        self.prompt = SQL_PROMPT
        self._command_queue = CommandQueue()
        self._session = session
        self._max_col_width = max_col_width
        self._transaction = None
        self._last_args = None

    def default(self, arg):
        "General shell command entry point"
        if arg != self._last_args:
            self._last_args = arg
            self._command_queue.ingest_line(arg.strip())
            [self._execute(cmd) for cmd in self._command_queue.commands()]
            if self._command_queue.has_fragment():
                self.prompt = SQL_CONTINUE_PROMPT
            else:
                self.prompt = SQL_PROMPT

    def do_bye(self, arg):
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
        except Exception as e:
            self._error("Executing query {}.\nDetails: {}".format(cmd, e))

    def _error(self, msg):
        "Prints an error message"
        print("\x1b[1;31;40mERROR: {}\x1b[0m".format(msg))