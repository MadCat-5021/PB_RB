# core/state_manager.py

from content.states import ALLOWED_TRANSITIONS
from core.events import STATE_CHANGED

class StateManager:
    def __init__(
        self,
        event_bus,
        initial_state="BOOT"
    ):
        self.event_bus = event_bus
        self.current_state = initial_state

    def get_state(self):
        return self.current_state

    def can_transition_to(
        self,
        new_state
    ):
        allowed_states = ALLOWED_TRANSITIONS.get(
            self.current_state,
            set()
        )
        return new_state in allowed_states

    def transition_to(
        self,
        new_state
    ):
        if not self.can_transition_to(new_state):
            raise ValueError(
                f"Invalid state transition: "
                f"{self.current_state} -> {new_state}"
            )
        previous_state = self.current_state
        self.current_state = new_state
        print(
            f"STATE: "
            f"{previous_state} -> {new_state}"
        )
        self.event_bus.publish(
            STATE_CHANGED,
            {
                "old_state": previous_state,
                "new_state": new_state
            }
        )
