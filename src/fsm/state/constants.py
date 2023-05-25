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
SQL_PROMPT = "analytic> "
SQL_CONTINUE_PROMPT = "        | "
SQL_OPTIONS = {
        "memberDisplayMode": "COMPACT",
        "zeroVisibility": "ELIMINATE",
        "nullVisibility": "ELIMINATE"
    }
SQL_STAGING_PROMPT = "staging> "
SQL_STAGING_CONTINUE_PROMPT = "       | "

SQL_TRANSACTION_PROMPT = "staging:tx> "
SQL_TRANSACTION_CONTINUE_PROMPT = "          | "

STATE_ANALYTIC = "analytic_state"
STATE_STAGING = "staging_state"
STATE_TRANSACTION = "transaction_state"

ATTR_SCHEMA = "schema"
VALUE_ANALYTIC = "analytic"
VALUE_STAGING = "staging"

PROJECT_PROD = "prod"
TRANSACTION_ID = "transactionId"

SCHEMA_MAP = {
    VALUE_ANALYTIC: STATE_ANALYTIC,
    VALUE_STAGING: STATE_STAGING
}
