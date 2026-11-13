from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from core.event_bus import EventBus
from core.events import (
    EXTRA_BALL_AWARDED,
    SHOOT_AGAIN_EXPIRED,
    SHOOT_AGAIN_STARTED
)
from gameplay.shoot_again_manager import ShootAgainManager


class Settings:
    def get(self, name):
        if name == "SHOOT_AGAIN_TIMEOUT":
            return 10
        raise KeyError(name)


class ShootAgainTests(unittest.TestCase):
    def test_first_launch_and_extra_ball_activate_or_refresh_timeout(self):
        event_bus = EventBus()
        expired = []
        event_bus.subscribe(
            SHOOT_AGAIN_EXPIRED,
            lambda *_: expired.append(True))
        manager = ShootAgainManager(event_bus, Settings())
        output = StringIO()

        with redirect_stdout(output):
            with patch("gameplay.shoot_again_manager.monotonic", return_value=0):
                event_bus.publish(SHOOT_AGAIN_STARTED, {})
        self.assertTrue(manager.is_active())

        with redirect_stdout(output):
            with patch("gameplay.shoot_again_manager.monotonic", return_value=9):
                event_bus.publish(EXTRA_BALL_AWARDED, {})
                manager.update()
        self.assertTrue(manager.is_active())
        self.assertEqual(expired, [])

        with redirect_stdout(output):
            with patch("gameplay.shoot_again_manager.monotonic", return_value=18.99):
                manager.update()
        self.assertTrue(manager.is_active())
        self.assertEqual(expired, [])

        with redirect_stdout(output):
            with patch("gameplay.shoot_again_manager.monotonic", return_value=19):
                manager.update()
        self.assertFalse(manager.is_active())
        self.assertEqual(expired, [True])
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "SHOOT AGAIN STARTED",
                "SHOOT AGAIN STARTED",
                "SHOOT AGAIN ENDED"
            ])


if __name__ == "__main__":
    unittest.main()
