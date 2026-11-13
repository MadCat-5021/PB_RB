import unittest
from unittest.mock import patch

from core.event_bus import EventBus
from core.state_manager import StateManager


class Settings:
    def get(self, name):
        if name == "HIGHSCORE_TIMEOUT":
            return 30
        raise KeyError(name)


class StateManagerTests(unittest.TestCase):
    def test_highscore_timeout_uses_configured_setting(self):
        with patch("core.state_manager.time", return_value=100):
            manager = StateManager(
                EventBus(),
                Settings(),
                initial_state="HIGHSCORE")

        with patch("core.state_manager.time", return_value=129):
            manager.check_timeouts()
        self.assertEqual(manager.get_state(), "HIGHSCORE")

        with patch("core.state_manager.time", return_value=130):
            manager.check_timeouts()
        self.assertEqual(manager.get_state(), "ACTIVE")


if __name__ == "__main__":
    unittest.main()
