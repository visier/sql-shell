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

from typing import Dict, Tuple
from visier.connector import VisierSession
from .state import State, AnalyticState, StagingState, TransactionState
from .state.constants import STATE_ANALYTIC, STATE_STAGING, STATE_TRANSACTION

class StateMachine:
    """
    The finite state machine for the SQL-like shell that ensures that
    SQL-like statements are executed in the corect context.
    """
    def __init__(self, states: Dict, initial_state: str):
        self._states = states
        self._state = self._states[initial_state]

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
        transition_req = self._state.execute(cmd)
        if transition_req is not None:
            self.transition_to(transition_req)

    def transition_to(self, transition_req: Tuple[str, object]):
        """
        Sets the current state
        """
        # TODO: set transition state parameters
        (new_state_name, params) = transition_req
        new_state = self._states[new_state_name]
        self._state = new_state


def mk_fsm(session: VisierSession, max_col_width: int, initial_state: str = STATE_ANALYTIC) -> StateMachine:
    """
    Creates a new state machine in the initial state
    """
    if initial_state not in [STATE_ANALYTIC, STATE_STAGING]:
        raise ValueError('Invalid initial state')
    
    states = {STATE_ANALYTIC: AnalyticState(session, max_col_width), 
              STATE_STAGING: StagingState(session),
              STATE_TRANSACTION: TransactionState(session)}
    return StateMachine(states, initial_state)
