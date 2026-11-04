# core/state_manager.py

class StateManager:

    def __init__(self):
        self.current_state = "BOOT"

    def get_state(self):
        return self.current_state

    def set_state(self, new_state):

        old_state = self.current_state
        self.current_state = new_state

        print(
            f"STATE CHANGE: {old_state} -> {new_state}"
        )