import re

class CommandQueue():
    "Ingests ;-separated command fragments and composes executable SQL-like statements"
    def __init__(self):
        self._queue = []
        self._fragment = ""

    def ingest_line(self, line: str):
        "Ingests a string and extracts complete commands or a fragment from it"
        cmds = re.split(""";(?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", line.strip())
        if len(cmds) > 1:
            first_cmd = cmds[0]
            if len(self._fragment) > 0:
                first_cmd = self._fragment + "\n" + first_cmd
                self._fragment = ""
            complete_cmds = [first_cmd] + cmds[1:-1]
            self._queue.extend(complete_cmds)
            self._fragment = cmds[-1].strip()
        else:
            if len(self._fragment) == 0:
                self._fragment = line
            else:
                self._fragment += "\n" + line


    def commands(self):
        "Generates a list of commands"
        for cmd in self._queue:
            yield cmd
        self._queue = []

    def has_fragment(self):
        "Returns true if the queue contains a partial command"
        return len(self._fragment) > 0