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
Visier SQL-like Read Eval Print Loop (REPL) constants.
"""

# SQL-like shell constants
SQL_INTRO = """
\x1b[1;32;40mWelcome to the Visier SQL-like Shell.
Type help or ? to list commands.

There are two available schemas: analytic and staging. Only one schema can be active at a time.
The currently active schema is indicated by the prompt.
Change the schema by using the 'SET' command. E.g.
SET schema TO staging;

Each SQL-like statement must be terminated with a semicolon (;) in order to execute.
\x1b[;;40m
"""
SQL_EXIT = "\x1b[1;32;40mClosing the application\x1b[0m"
