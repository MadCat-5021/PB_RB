# input/input_manager.py

from core.events import SWITCH_PRESSED


class InputManager:

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def run(self):

        while True:

            key = input("Switch: ").strip().upper()

            self.event_bus.publish(
                SWITCH_PRESSED,
                {
                    "switch": key
                }
            )