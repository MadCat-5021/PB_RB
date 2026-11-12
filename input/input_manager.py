# input/input_manager.py

from threading import Thread
from core.events import SWITCH_PRESSED, SWITCH_RELEASED

class InputManager:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def input_loop(self):
        while True:
            key = input(
                "Switch: "
            ).strip().upper()
            if not key:
                continue
            command, _, switch = key.partition(" ")
            if command == "RELEASE":
                if not switch.strip():
                    continue
                event_type = SWITCH_RELEASED
                key = switch.strip()
            else:
                event_type = SWITCH_PRESSED
            self.event_bus.publish(
                event_type,
                {
                    "switch": key
                }
            )

    def run(self):
        Thread(
            target=self.input_loop,
            daemon=True
        ).start()