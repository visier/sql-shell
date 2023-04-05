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
SQL_PROMPT = "\x1b[1;34;40msql> \x1b[1;37;40m"
SQL_CONTINUE_PROMPT = "\x1b[1;34;40m   | \x1b[1;37;40m"
SQL_BYE = "\x1b[1;32;40mClosing the application\x1b[0m"
SQL_TABLE_START = "\n\x1b[1;37;40m"
SQL_TABLE_END = "\x1b[;;40m\n"
SQL_OPTIONS = {
        "memberDisplayMode": "COMPACT",
        "zeroVisibility": "ELIMINATE",
        "nullVisibility": "ELIMINATE"
    }
