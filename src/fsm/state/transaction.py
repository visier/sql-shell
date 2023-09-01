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
Defines the FSM State for executing SQL-like commands within the context of a transaction.
"""

from typing import Tuple
import re
from visier.connector import VisierSession, QueryExecutionError
from visier.api import DirectIntakeApiClient
from .state import State
from .constants import (SQL_TRANSACTION_CONTINUE_PROMPT,
                        STATE_STAGING,
                        TRANSACTION_ID)


class TransactionState(State):
    """State for executing SQL-like commands within the context of a transaction."""
    def __init__(self, session: VisierSession) -> None:
        super().__init__()
        self._client = DirectIntakeApiClient(session, raise_on_error=True)
        self._copy = re.compile(r'^\s*copy\s+(?P<table_name>\w+)\s+from\s+\'(?P<file_path>[^\']*)\'\s*$', re.IGNORECASE)

    def prompt(self) -> str:
        return f"staging:{self._get_transaction_id()}> "

    def continue_prompt(self) -> str:
        return SQL_TRANSACTION_CONTINUE_PROMPT

    def execute(self, cmd: str) -> Tuple[str, object]:
        if self._is_upload_cmd(cmd):
            return self._execute_upload(cmd)
        if self._is_commit_cmd(cmd):
            return self._execute_commit()
        if self._is_rollback_cmd(cmd):
            return self._execute_rollback()
        self._error(f"Invalid command: {cmd}")
        return None

    def _is_upload_cmd(self, cmd: str) -> bool:
        return self._copy.match(cmd) is not None

    def _is_rollback_cmd(self, cmd: str) -> bool:
        return cmd.lower().startswith("rollback")

    def _is_commit_cmd(self, cmd: str) -> bool:
        return cmd.lower().startswith("commit")

    def _execute_upload(self, cmd: str) -> None:
        match = self._copy.match(cmd)
        object_name = match.group("table_name")
        file_path = match.group("file_path")
        try:
            self._client.upload_file(self._get_transaction_id(), object_name, file_path)
        except QueryExecutionError as query_exec_error:
            self._error(f"Could not upload data: {query_exec_error}")
        except FileNotFoundError as file_not_found_error:
            self._error(f"File not found: {file_not_found_error}")

    def _execute_commit(self) -> Tuple[str, object]:
        try:
            self._client.commit_transaction(self._get_transaction_id())
        except QueryExecutionError as query_exec_error:
            self._error(f"Could not commit transaction: {query_exec_error}")
        return (STATE_STAGING, {})

    def _execute_rollback(self) -> Tuple[str, object]:
        try:
            self._client.rollback_transaction(self._get_transaction_id())
        except QueryExecutionError as query_exec_error:
            self._error(f"Could not rollback transaction: {query_exec_error}")
        return (STATE_STAGING, {})

    def _get_transaction_id(self) -> str:
        try:
            transaction_id = self._params[TRANSACTION_ID]
            return transaction_id
        except KeyError as key_error:
            raise KeyError("No transaction id found in the transaction context") from key_error
