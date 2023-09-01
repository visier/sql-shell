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
        Sets the current state and initialize with parameter values where applicable
        """
        (new_state_name, params) = transition_req
        new_state: State = self._states[new_state_name]
        new_state.put_parameters(params)
        self._state = new_state


def mk_fsm(session: VisierSession,
           max_col_width: int,
           initial_state: str = STATE_ANALYTIC) -> StateMachine:
    """
    Creates a new state machine in the initial state
    """
    if initial_state not in [STATE_ANALYTIC, STATE_STAGING]:
        raise ValueError('Invalid initial state')

    states = {STATE_ANALYTIC: AnalyticState(session, max_col_width),
              STATE_STAGING: StagingState(session),
              STATE_TRANSACTION: TransactionState(session)}
    return StateMachine(states, initial_state)
