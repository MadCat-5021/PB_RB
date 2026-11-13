import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from core.event_bus import EventBus
from core.events import (
    BALL_LAUNCHED,
    BALL_READY,
    BALL_STARTED,
    LAUNCH_BONUS_AWARDED,
    LAUNCH_COMPLETED,
    LAUNCH_COUNTDOWN_TICK,
    LAUNCH_SEQUENCE,
    PRE_TURN,
    SHOOT_AGAIN_STARTED,
    LAUNCH_ZERO,
    SWITCH_RELEASED,
)
from gameplay.game import Game
from gameplay.launch_manager import LaunchManager
from gameplay.player_manager import PlayerManager
from gameplay.score_manager import ScoreManager
from input.input_manager import InputManager


class Settings:
    def __init__(self, has_launch_sequence):
        self.has_launch_sequence = has_launch_sequence

    def get(self, name):
        if name == "MACHINE_HAS_LAUNCH_SEQUENCE":
            return self.has_launch_sequence
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class BallLaunchTests(unittest.TestCase):
    def make_game(self, has_launch_sequence):
        game = Game.__new__(Game)
        game.event_bus = EventBus()
        game.settings = Settings(has_launch_sequence)
        game.player_manager = PlayerManager(game.settings)
        game.player_manager.start_game()
        game.first_ball_of_turn = True
        game.first_ball_launched = False
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

    def test_countdown_waits_randomly_after_one_before_zero(self):
        event_bus = EventBus()
        countdown = []
        zero = []
        event_bus.subscribe(
            LAUNCH_COUNTDOWN_TICK,
            lambda _event, data: countdown.append(data["count"]))
        event_bus.subscribe(
            LAUNCH_ZERO,
            lambda *_: zero.append(True))
        manager = LaunchManager(event_bus)

        with patch("gameplay.launch_manager.monotonic", return_value=10):
            with patch("gameplay.launch_manager.uniform", return_value=1.5):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        self.assertEqual(countdown, [5])

        with patch("gameplay.launch_manager.monotonic", return_value=14):
            manager.update()
        self.assertEqual(countdown, [5, 4, 3, 2, 1])
        self.assertEqual(zero, [])

        with patch("gameplay.launch_manager.monotonic", return_value=15.49):
            manager.update()
        self.assertEqual(zero, [])

        with patch("gameplay.launch_manager.monotonic", return_value=15.5):
            manager.update()
        self.assertEqual(zero, [True])

    def test_reaction_bonus_is_separate_and_clamped_to_window(self):
        event_bus = EventBus()
        launch_bonuses = []
        event_bus.subscribe(
            LAUNCH_BONUS_AWARDED,
            lambda _event, data: launch_bonuses.append(data))
        player_manager = PlayerManager(Settings(True))
        player_manager.start_game()
        score_manager = ScoreManager(event_bus, player_manager)
        launch_manager = LaunchManager(event_bus)

        with patch("gameplay.launch_manager.monotonic", return_value=0):
            with patch("gameplay.launch_manager.uniform", return_value=1):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        with patch("gameplay.launch_manager.monotonic", return_value=7.5):
            event_bus.publish(BALL_LAUNCHED, {})

        self.assertEqual(launch_bonuses[0]["points"], 2750)
        self.assertEqual(score_manager.get_score(), 0)
        self.assertEqual(score_manager.get_bonus(), 2750)

        with patch("gameplay.launch_manager.monotonic", return_value=10):
            with patch("gameplay.launch_manager.uniform", return_value=1):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        with patch("gameplay.launch_manager.monotonic", return_value=20.1):
            event_bus.publish(BALL_LAUNCHED, {})

        self.assertEqual(len(launch_bonuses), 1)
        self.assertEqual(score_manager.get_bonus(), 2750)

    def test_launch_bonus_window_includes_zero_and_five_seconds(self):
        event_bus = EventBus()
        bonuses = []
        event_bus.subscribe(
            LAUNCH_BONUS_AWARDED,
            lambda _event, data: bonuses.append(data["points"]))
        LaunchManager(event_bus)

        with patch("gameplay.launch_manager.monotonic", return_value=0):
            with patch("gameplay.launch_manager.uniform", return_value=1):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        with patch("gameplay.launch_manager.monotonic", return_value=4.999):
            event_bus.publish(BALL_LAUNCHED, {})
        self.assertEqual(bonuses, [])

        with patch("gameplay.launch_manager.monotonic", return_value=10):
            with patch("gameplay.launch_manager.uniform", return_value=1):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        with patch("gameplay.launch_manager.monotonic", return_value=15):
            event_bus.publish(BALL_LAUNCHED, {})
        self.assertEqual(bonuses, [5000])

        with patch("gameplay.launch_manager.monotonic", return_value=20):
            with patch("gameplay.launch_manager.uniform", return_value=1):
                event_bus.publish(LAUNCH_SEQUENCE, {})
        with patch("gameplay.launch_manager.monotonic", return_value=30):
            event_bus.publish(BALL_LAUNCHED, {})
        self.assertEqual(bonuses, [5000, 500])

    def test_launch_result_messages_only_show_for_launch_sequences(self):
        event_bus = EventBus()
        LaunchManager(event_bus)

        with redirect_stdout(StringIO()) as output:
            event_bus.publish(BALL_LAUNCHED, {})
        self.assertEqual(output.getvalue(), "")

        for launch_at, expected_message in (
            (4.9, "Start infringement"),
            (5, "Quick off the line, BONUS: 5000"),
            (10.1, "Too slow"),
        ):
            with self.subTest(launch_at=launch_at):
                with patch("gameplay.launch_manager.monotonic", return_value=0):
                    with patch("gameplay.launch_manager.uniform", return_value=1):
                        event_bus.publish(LAUNCH_SEQUENCE, {})
                output = StringIO()
                with patch(
                    "gameplay.launch_manager.monotonic",
                    return_value=launch_at
                ):
                    with redirect_stdout(output):
                        event_bus.publish(BALL_LAUNCHED, {})
                self.assertIn(expected_message, output.getvalue())

    def test_shoot_again_starts_only_after_first_launch_per_turn(self):
        game = self.make_game(has_launch_sequence=False)
        starts = []
        game.event_bus.subscribe(
            SHOOT_AGAIN_STARTED,
            lambda *_: starts.append(True))

        game.on_pre_turn(PRE_TURN, {})
        game.waiting_for_ball_launched = True
        game.on_ball_launched(BALL_LAUNCHED, {})
        game.waiting_for_ball_launched = True
        game.on_ball_launched(BALL_LAUNCHED, {})
        self.assertEqual(starts, [True])

        game.on_pre_turn(PRE_TURN, {})
        game.waiting_for_ball_launched = True
        game.on_ball_launched(BALL_LAUNCHED, {})
        self.assertEqual(starts, [True, True])


if __name__ == "__main__":
    unittest.main()
