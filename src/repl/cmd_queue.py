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
Command queue module that composes SQL-like statements from fragments.
"""

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

    def fragment(self):
        "Returns the current fragment"
        return self._fragment

    def has_fragment(self):
        "Returns true if the queue contains a partial command"
        return len(self._fragment) > 0
