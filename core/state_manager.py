# core/state_manager.py

from time import time

from core.events import (
    SWITCH_PRESSED,
    STATE_CHANGED
)

from content.states import (
    MACHINE_STATES,
    ALLOWED_TRANSITIONS
)


class StateManager:

    def __init__(
        self,
        event_bus,
        settings,
        initial_state="BOOT"
    ):

        if initial_state not in MACHINE_STATES:
            raise ValueError(
                f"Invalid state: "
                f"{initial_state}"
            )

        self.event_bus = event_bus
        self.settings = settings

        self.state = initial_state

        self.last_activity = time()

        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

        print(
            f"STATE: {self.state}"
        )

    def on_switch_pressed(
        self,
        event_type,
        data
    ):

        self.register_activity()

        if self.state in {
            "PASSIVE",
            "ATTRACT",
            "HIGHSCORE"
        }:
            self.set_state(
                "ACTIVE"
            )

    def register_activity(
        self
    ):
        self.last_activity = time()

    def get_last_activity(
        self
    ):
        return self.last_activity

    def get_state(
        self
    ):
        return self.state

    def is_state(
        self,
        state
    ):
        return self.state == state

    def can_transition(
        self,
        new_state
    ):

        if self.state not in ALLOWED_TRANSITIONS:
            return False

        return (
            new_state
            in ALLOWED_TRANSITIONS[
                self.state
            ]
        )

    def set_state(
        self,
        new_state
    ):

        if new_state == self.state:
            return True

        if not self.can_transition(
            new_state
        ):

            print(
                f"INVALID TRANSITION: "
                f"{self.state} -> "
                f"{new_state}"
            )

            return False

        old_state = self.state

        self.state = new_state

        print(
            f"STATE: "
            f"{old_state} -> "
            f"{new_state}"
        )

        self.event_bus.publish(
            STATE_CHANGED,
            {
                "old_state": old_state,
                "new_state": new_state
            }
        )

        return True

    def check_timeouts(
        self
    ):

        if (
            self.state == "ACTIVE"
            and time() - self.last_activity
            >= self.settings.get(
                "ACTIVE_TIMEOUT"
            )
        ):
            self.set_state(
                "PASSIVE"
            )