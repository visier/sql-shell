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
