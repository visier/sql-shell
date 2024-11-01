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
Command queue module that composes SQL-like statements from fragments.
"""

import re


class CommandQueue():
    "Ingests ;-separated command fragments and composes executable SQL-like statements"
    def __init__(self):
        self._queue = []
        self._fragment = ""
        self._seq = re.compile(r""";(?=(?:[^'"]|'[^']*'|"[^"]*")*$)""")

    def ingest_line(self, line: str):
        "Ingests a string and extracts complete commands or a fragment from it"
        cmds = self._seq.split(line.strip())
        if len(cmds) > 1:
            first_cmd = cmds[0]
            if len(self._fragment) > 0:
                first_cmd = self._fragment + "\n" + first_cmd
                self._fragment = ""
            complete_cmds = [first_cmd] + [cmd.strip() for cmd in cmds[1:-1]]
            self._queue.extend(complete_cmds)
            self._fragment = cmds[-1].strip()
        else:
            if len(self._fragment) == 0:
                self._fragment = line
            else:
                self._fragment += "\n" + line


    def commands(self):
        "Generates a list of commands"
        yield from self._queue
        self._queue = []

    def fragment(self):
        "Returns the current fragment"
        return self._fragment

    def has_fragment(self):
        "Returns true if the queue contains a partial command"
        return len(self._fragment) > 0
