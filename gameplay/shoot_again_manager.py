from time import monotonic

from core.events import (
    EXTRA_BALL_AWARDED,
    SHOOT_AGAIN_EXPIRED,
    SHOOT_AGAIN_STARTED
)


class ShootAgainManager:

    def __init__(
        self,
        event_bus,
        settings):
        self.event_bus = event_bus
        self.settings = settings
        self.active = False
        self.expires_at = None
        self.event_bus.subscribe(
            SHOOT_AGAIN_STARTED,
            self.on_shoot_again_started)
        self.event_bus.subscribe(
            EXTRA_BALL_AWARDED,
            self.on_extra_ball_awarded)

    def update(self):
        if not self.active or monotonic() < self.expires_at:
            return
        self.deactivate()

    def deactivate(self):
        if not self.active:
            return
        self.active = False
        self.expires_at = None
        print("SHOOT AGAIN ENDED")
        self.event_bus.publish(SHOOT_AGAIN_EXPIRED, {})

    def is_active(self):
        return self.active

    def on_shoot_again_started(
        self,
        _event_type,
        _data):
        self._activate()

    def on_extra_ball_awarded(
        self,
        _event_type,
        _data):
        self._activate()

    def _activate(self):
        self.active = True
        self.expires_at = (
            monotonic()
            + self.settings.get("SHOOT_AGAIN_TIMEOUT")
        )
        print("SHOOT AGAIN STARTED")
