from content.states import ALLOWED_TRANSITIONS

class StateManager:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.current_state = "BOOT"

    def transition_to(self, new_state):
        allowed = ALLOWED_TRANSITIONS.get(
            self.current_state,
            set()
        )
        if new_state not in allowed:
            raise ValueError(...)
        old_state = self.current_state
        self.current_state = new_state
        print(
            f"STATE: {old_state} -> {new_state}"
        )
