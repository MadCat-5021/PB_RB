# gameplay/ball_manager.py

from time import time
from core.events import (
    BALL_SUPPLY,
    BALL_READY,
    SWITCH_PRESSED)


class BallManager:

    def __init__(
        self,
        event_bus,
        coil_manager,
        target_manager,
        settings):
        self.event_bus = event_bus
        self.coil_manager = coil_manager
        self.target_manager = target_manager
        self.waiting_for_ball = False
        self.last_supply_attempt = 0
        self.settings = settings
        self.event_bus.subscribe(BALL_SUPPLY,self.on_ball_supply)
        self.event_bus.subscribe(SWITCH_PRESSED,self.on_switch_pressed)

    def on_ball_supply(
        self,
        event_type,
        data):
        print("BALL MANAGER: SUPPLY")
        self.waiting_for_ball = True
        self.supply_attempt()

    def supply_attempt(self):

        self.last_supply_attempt = time()

        self.coil_manager.pulse(
            "TROUGH_COIL",
            100)

    def on_switch_pressed(
        self,
        event_type,
        data):
        if not self.waiting_for_ball:
            return
        if data["switch"] != "PLUNGER":
            return
        self.waiting_for_ball = False
        print("BALL READY")
        self.event_bus.publish(
            BALL_READY,
            {})

    def check_supply(self):
        if not self.waiting_for_ball:
            return
        if (time() - self.last_supply_attempt < self.settings.get("RETRY_BALL_SUPPLY")):
            return
        print("BALL RETRY")
        self.supply_attempt()