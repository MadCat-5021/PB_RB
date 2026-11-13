import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from core.event_bus import EventBus
from core.events import (
    BALL_LAUNCHED,
    BALL_READY,
    BALL_STARTED,
    LAUNCH_COMPLETED,
    LAUNCH_SEQUENCE,
    SWITCH_RELEASED,
)
from gameplay.game import Game
from gameplay.launch_manager import LaunchManager
from input.input_manager import InputManager


class Settings:
    def __init__(self, has_launch_sequence):
        self.has_launch_sequence = has_launch_sequence

    def get(self, name):
        if name == "MACHINE_HAS_LAUNCH_SEQUENCE":
            return self.has_launch_sequence
        raise KeyError(name)


class BallLaunchTests(unittest.TestCase):
    def make_game(self, has_launch_sequence):
        game = Game.__new__(Game)
        game.event_bus = EventBus()
        game.settings = Settings(has_launch_sequence)
        game.first_ball_of_turn = True
        game.waiting_for_ball_launched = False
        game.event_bus.subscribe(BALL_LAUNCHED, game.on_ball_launched)
        return game

    def test_both_launch_paths_wait_for_ball_launched(self):
        for has_launch_sequence in (True, False):
            with self.subTest(has_launch_sequence=has_launch_sequence):
                game = self.make_game(has_launch_sequence)
                started = []
                sequences = []
                game.event_bus.subscribe(
                    BALL_STARTED,
                    lambda *_: started.append(True))
                game.event_bus.subscribe(
                    LAUNCH_SEQUENCE,
                    lambda *_: sequences.append(True))

                game.on_ball_ready(BALL_READY, {})

                self.assertTrue(game.waiting_for_ball_launched)
                self.assertEqual(sequences, [True] if has_launch_sequence else [])
                self.assertEqual(started, [])

                game.event_bus.publish(BALL_LAUNCHED, {})
                game.event_bus.publish(BALL_LAUNCHED, {})

                self.assertFalse(game.waiting_for_ball_launched)
                self.assertEqual(started, [True])

    def test_plunger_release_signals_ball_launched(self):
        for has_launch_sequence in (True, False):
            with self.subTest(has_launch_sequence=has_launch_sequence):
                game = self.make_game(has_launch_sequence)
                started = []
                game.event_bus.subscribe(
                    BALL_STARTED,
                    lambda *_: started.append(True))
                game.on_ball_ready(BALL_READY, {})

                game.on_switch_released(
                    SWITCH_RELEASED,
                    {"switch": "PLUNGER"})

                self.assertEqual(started, [True])
                self.assertFalse(game.waiting_for_ball_launched)

    def test_console_launched_command_publishes_signal(self):
        game = self.make_game(has_launch_sequence=True)
        game.waiting_for_ball_launched = True
        output = StringIO()

        with patch("builtins.input", side_effect=["LAUNCHED", KeyboardInterrupt]):
            with redirect_stdout(output):
                with self.assertRaises(KeyboardInterrupt):
                    InputManager(game.event_bus).input_loop()

        self.assertIn("LAUNCHED COMMAND RECEIVED", output.getvalue())
        self.assertIn("BALL STARTED", output.getvalue())
        self.assertFalse(game.waiting_for_ball_launched)

    def test_launch_sequence_completion_publishes_ball_launched(self):
        event_bus = EventBus()
        launched = []
        event_bus.subscribe(
            BALL_LAUNCHED,
            lambda *_: launched.append(True))
        LaunchManager(event_bus)

        event_bus.publish(LAUNCH_COMPLETED, {})

        self.assertEqual(launched, [True])


if __name__ == "__main__":
    unittest.main()
