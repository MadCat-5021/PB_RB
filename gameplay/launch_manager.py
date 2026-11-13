# gameplay/launch_manager.py

from random import uniform
from time import monotonic

from core.events import (
    BALL_LAUNCHED,
    LAUNCH_BONUS_AWARDED,
    LAUNCH_COMPLETED,
    LAUNCH_COUNTDOWN_TICK,
    LAUNCH_SEQUENCE,
    LAUNCH_ZERO
)


class LaunchManager:

    def __init__(
        self,
        event_bus):
        self.event_bus = event_bus
        self.countdown_started_at = None
        self.zero_at = None
        self.countdown_value = None
        self.zero_announced = False
        self.event_bus.subscribe(LAUNCH_SEQUENCE,self.on_launch_sequence)
        self.event_bus.subscribe(LAUNCH_COMPLETED,self.on_launch_complete)
        self.event_bus.subscribe(BALL_LAUNCHED,self.on_ball_launched)

    def update(self):
        if self.countdown_started_at is None:
            return
        self._advance_countdown(monotonic())

    def _advance_countdown(self, now):
        while (
            self.countdown_value > 1
            and now >= self.countdown_started_at + 6 - self.countdown_value
        ):
            self.countdown_value -= 1
            self._publish_countdown_tick()

        if not self.zero_announced and now >= self.zero_at:
            self.zero_announced = True
            print("LAUNCH COUNTDOWN: 0")
            self.event_bus.publish(LAUNCH_ZERO, {})

    def on_launch_sequence(
        self,
        event_type,
        data):
        print("LAUNCH SEQUENCE STARTED")
        self.countdown_started_at = monotonic()
        self.zero_at = (
            self.countdown_started_at
            + 4
            + uniform(0.8, 2.0)
        )
        self.countdown_value = 5
        self.zero_announced = False
        self._publish_countdown_tick()

    def _publish_countdown_tick(self):
        print(f"LAUNCH COUNTDOWN: {self.countdown_value}")
        self.event_bus.publish(
            LAUNCH_COUNTDOWN_TICK,
            {"count": self.countdown_value})

    def on_launch_complete(
        self,
        event_type,
        data):
        print("BALL LAUNCHED")
        self.event_bus.publish(
            BALL_LAUNCHED,
            {})

    def on_ball_launched(
        self,
        _event_type,
        _data):
        if self.countdown_started_at is None:
            return

        launched_at = monotonic()
        self._advance_countdown(launched_at)
        if self.zero_at <= launched_at <= self.zero_at + 5:
            reaction_time = launched_at - self.zero_at
            bonus = 5000 - int(reaction_time * 90) * 10
            self.event_bus.publish(
                LAUNCH_BONUS_AWARDED,
                {
                    "points": bonus,
                    "reaction_time": reaction_time
                })
            print(f"Quick off the line, BONUS: {bonus}")
        elif launched_at < self.zero_at:
            print("Start infringement")
        else:
            print("Too slow")

        self.countdown_started_at = None
        self.zero_at = None
        self.countdown_value = None
        self.zero_announced = False