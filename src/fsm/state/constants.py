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
SQL_PROMPT = "analytic> "
SQL_CONTINUE_PROMPT = "        | "
SQL_OPTIONS = {
        "memberDisplayMode": "COMPACT",
        "zeroVisibility": "ELIMINATE",
        "nullVisibility": "ELIMINATE"
    }
SQL_STAGING_PROMPT = "staging> "
SQL_STAGING_CONTINUE_PROMPT = "       | "

SQL_TRANSACTION_CONTINUE_PROMPT = "       | "

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
