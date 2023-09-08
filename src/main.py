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
Visier SQL-like Shell provides a REPL interface to Visier's SQL-like query language.
"""

import argparse
from visier.connector import add_auth_arguments, make_auth
from visier.connector import VisierSession
from repl import SqlLikeShell
from fsm.state.constants import VALUE_ANALYTIC, VALUE_STAGING
from dotenv import dotenv_values


def main():
    "Main entrypoint for the visier-sqllike-shell command."
    parser = argparse.ArgumentParser(description="Visier SQL-like Shell")
    add_auth_arguments(parser)
    parser.add_argument("-s", "--schema", help="The initial schema to use",
                        choices=[VALUE_ANALYTIC, VALUE_STAGING], default=VALUE_ANALYTIC)
    parser.add_argument("-w", "--width", help="Maximum column width", type=int, default=30)

    args = parser.parse_args()
    env_creds = dotenv_values()
    auth = make_auth(args=args, env_values=env_creds)
    with VisierSession(auth) as session:
        SqlLikeShell(session, args.width, args.schema).cmdloop()

if __name__ == "__main__":
    main()
