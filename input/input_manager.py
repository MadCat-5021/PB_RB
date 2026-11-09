# input/input_manager.py

from threading import Thread
from core.events import SWITCH_PRESSED

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
            self.event_bus.publish(
                SWITCH_PRESSED,
                {
                    "switch": key
                }
            )

    def run(self):
        Thread(
            target=self.input_loop,
            daemon=True
        ).start()