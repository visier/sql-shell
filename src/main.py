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
Visier SQL-like Shell provides a REPL interface to Visier's SQL-like query language.
"""

import argparse
from visier.connector import add_auth_arguments, make_auth
from visier.connector import VisierSession
from repl import SqlLikeShell
from fsm.state.constants import VALUE_ANALYTIC, VALUE_STAGING


def main():
    "Main entrypoint for the visier-sqllike-shell command."
    parser = argparse.ArgumentParser(description="Visier SQL-like Shell")
    add_auth_arguments(parser)
    parser.add_argument("-s", "--schema", help="The initial schema to use",
                        choices=[VALUE_ANALYTIC, VALUE_STAGING], default=VALUE_ANALYTIC)
    parser.add_argument("-w", "--width", help="Maximum column width", type=int, default=30)
    args = parser.parse_args()

    auth = make_auth(args)

    with VisierSession(auth) as session:
        SqlLikeShell(session, args.width, args.schema).cmdloop()

if __name__ == "__main__":
    main()
