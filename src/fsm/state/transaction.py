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
Defines the FSM State for executing SQL-like commands within the context of a transaction.
"""

from typing import Tuple
from requests import Session, Response
from visier.connector import VisierSession, QueryExecutionError
from .state import State
from .constants import (PROJECT_PROD,
                        SQL_TRANSACTION_PROMPT,
                        SQL_TRANSACTION_CONTINUE_PROMPT,
                        STATE_STAGING,
                        TRANSACTION_ID)


class TransactionState(State):
    """State for executing SQL-like commands within the context of a transaction."""
    def __init__(self, session: VisierSession) -> None:
        super().__init__()
        self._session = session
        # self._params = {}

    def prompt(self) -> str:
        return SQL_TRANSACTION_PROMPT

    def continue_prompt(self) -> str:
        return SQL_TRANSACTION_CONTINUE_PROMPT

    # def put_parameters(self, params: object) -> None:
    #     print(f"Setting parameters: {params}")
    #     self._params = params

    def execute(self, cmd: str) -> None | Tuple[str, object]:
        """
        Main entry point for executing a command while in a transactional context.
        """
        if self._is_commit_cmd(cmd):
            return self._execute_commit()
        if self._is_rollback_cmd(cmd):
            return self._execute_rollback()
        self._error(f"Invalid command: {cmd}")
        return None

    def _is_rollback_cmd(self, cmd: str) -> bool:
        return cmd.lower().startswith("rollback")

    def _is_commit_cmd(self, cmd: str) -> bool:
        return cmd.lower().startswith("commit")

    def _execute_commit(self) -> Tuple[str, object]:
        def _api_commit(session: Session) -> Response:
            transaction_id = self._get_transaction_id()
            return session.post(f"{self._session._auth.host}/v1/data/directloads/{PROJECT_PROD}/transactions/{transaction_id}")
        try:
            self._session.execute(_api_commit)
        except QueryExecutionError as query_exec_error:
            self._error(f"Could not commit transaction: {query_exec_error}")
        return (STATE_STAGING, {})

    def _execute_rollback(self) -> Tuple[str, object]:
        try:
            self._session.execute(self._api_rollback)
        except QueryExecutionError as query_exec_error:
            self._error(f"Could not rollback transaction: {query_exec_error}")
        return (STATE_STAGING, {})

    def _api_rollback(self, session: Session) -> Response:
        transaction_id = self._get_transaction_id()
        return session.delete(f"{self._session._auth.host}/v1/data/directloads/{PROJECT_PROD}/transactions/{transaction_id}")

    def _get_transaction_id(self) -> str:
        try:
            transaction_id = self._params[TRANSACTION_ID]
            return transaction_id
        except KeyError as key_error:
            raise KeyError("No transaction id found in the transaction context") from key_error
