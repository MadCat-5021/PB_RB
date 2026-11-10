# gameplay/control_manager.py

from core.events import (
    SWITCH_PRESSED,
    CREDIT_ADDED,
    START_REQUESTED,
    GAME_LAUNCH_REQUESTED)

class ControlManager:

    def __init__(
        self,
        event_bus):

        self.event_bus = event_bus
        self.credits = 0

        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed)

    def on_switch_pressed(
        self,
        event_type,
        data):
        switch = data["switch"]
        print(f"CONTROL: {switch}")
        if switch == "CREDIT_BUTTON":
            self.credits += 1
            self.event_bus.publish(
                CREDIT_ADDED,
                {
                    "credits":
                    self.credits
                })
        elif switch == "START_BUTTON":
            self.event_bus.publish(
                START_REQUESTED,
                {
                    "credits":
                    self.credits
                })
            print("START_REQUESTED PUBLISHED")
        elif switch in {"LEFT_FLIPPER_BUTTON","RIGHT_FLIPPER_BUTTON"}:
            self.event_bus.publish(
                GAME_LAUNCH_REQUESTED)

    def get_credits(self):
        return self.credits