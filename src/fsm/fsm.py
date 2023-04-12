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
The finite state machine for the SQL-like shell that ensures that
SQL-like statements are executed in the corect context.
"""

from visier.connector import VisierSession
from .state import State
from .state.analytic import AnalyticState

class StateMachine:
    """
    The finite state machine for the SQL-like shell that ensures that
    SQL-like statements are executed in the corect context.
    """
    def __init__(self, initial_state: State):
        self._state = initial_state

    def prompt(self) -> str:
        """
        Returns the prompt for the current state
        """
        return self._state.prompt()

    def continue_prompt(self) -> str:
        """
        Returns the prompt for the current state
        """
        return self._state.continue_prompt()

    def execute(self, cmd: str):
        """
        Executes a command in the current state
        """
        self._state.execute(cmd)

    def transition_to(self, state: State):
        """
        Sets the current state
        """
        self._state = state

def mk_fsm(session: VisierSession, max_col_width: int) -> StateMachine:
    """
    Creates a new state machine in the initial state
    """
    return StateMachine(AnalyticState(session, max_col_width))
