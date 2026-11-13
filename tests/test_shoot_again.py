from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from core.event_bus import EventBus
from core.events import (
    BALL_DRAINED,
    BALL_LAUNCHED,
    BALL_READY,
    BALL_STARTED,
    BALL_SUPPLY,
    EXTRA_BALL_AWARDED,
    LAUNCH_SEQUENCE,
    SHOOT_AGAIN_EXPIRED,
    SHOOT_AGAIN_STARTED,
    SWITCH_PRESSED,
    TURN_ENDED
)
from gameplay.game import Game
from gameplay.shoot_again_manager import ShootAgainManager


class Settings:
    def get(self, name):
        if name == "SHOOT_AGAIN_TIMEOUT":
            return 10
        if name == "MACHINE_HAS_LAUNCH_SEQUENCE":
            return True
        if name == "GAME_START_TIMEOUT":
            return 0
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

    def test_ball_drain_consumes_shoot_again_then_extra_ball_once_each(self):
        game = self.make_game()
        supplies = []
        started = []
        turns_ended = []
        launch_sequences = []
        game.event_bus.subscribe(
            BALL_SUPPLY,
            lambda *_: supplies.append(True))
        game.event_bus.subscribe(
            BALL_STARTED,
            lambda *_: started.append(True))
        game.event_bus.subscribe(
            TURN_ENDED,
            lambda *_: turns_ended.append(True))
        game.event_bus.subscribe(
            LAUNCH_SEQUENCE,
            lambda *_: launch_sequences.append(True))

        with patch("gameplay.shoot_again_manager.monotonic", return_value=0):
            game.event_bus.publish(EXTRA_BALL_AWARDED, {})
        self.assertTrue(game.shoot_again_manager.is_active())
        self.assertTrue(game.extra_ball_awarded)

        game.event_bus.publish(BALL_DRAINED, {})
        self.assertEqual(supplies, [True])
        self.assertFalse(game.shoot_again_manager.is_active())
        self.assertTrue(game.extra_ball_awarded)
        self.assertEqual(turns_ended, [])
        game.event_bus.publish(BALL_READY, {})
        self.assertEqual(launch_sequences, [])
        self.assertTrue(game.waiting_for_ball_launched)
        game.event_bus.publish(BALL_LAUNCHED, {})
        self.assertFalse(game.waiting_for_ball_launched)
        self.assertEqual(started, [True])

        game.event_bus.publish(BALL_DRAINED, {})
        self.assertEqual(supplies, [True, True])
        self.assertFalse(game.extra_ball_awarded)
        self.assertEqual(turns_ended, [])
        game.event_bus.publish(BALL_READY, {})
        self.assertEqual(launch_sequences, [])
        self.assertTrue(game.waiting_for_ball_launched)
        game.event_bus.publish(BALL_LAUNCHED, {})
        self.assertFalse(game.waiting_for_ball_launched)
        self.assertEqual(started, [True, True])

    def test_ball_drain_ends_turn_without_awards(self):
        game = self.make_game()
        supplies = []
        turns_ended = []
        game.event_bus.subscribe(
            BALL_SUPPLY,
            lambda *_: supplies.append(True))
        game.event_bus.subscribe(
            TURN_ENDED,
            lambda *_: turns_ended.append(True))

        game.event_bus.publish(BALL_DRAINED, {})

        self.assertEqual(supplies, [])
        self.assertEqual(turns_ended, [True])
        self.assertFalse(game.ball_launched)
        game.check_game_start()
        self.assertEqual(supplies, [])

    def test_drain_switch_publishes_ball_drained(self):
        game = self.make_game()
        turns_ended = []
        game.event_bus.subscribe(
            TURN_ENDED,
            lambda *_: turns_ended.append(True))

        game.event_bus.publish(
            SWITCH_PRESSED,
            {"switch": "DRAIN"})
        game.event_bus.publish(
            SWITCH_PRESSED,
            {"switch": "DROP_1"})

        self.assertEqual(turns_ended, [True])

    def make_game(self):
        game = Game.__new__(Game)
        game.event_bus = EventBus()
        game.settings = Settings()
        game.game_active = True
        game.ball_launched = True
        game.initial_ball_pending = False
        game.game_started_at = 0
        game.first_ball_of_turn = False
        game.first_ball_launched = True
        game.waiting_for_ball_launched = False
        game.extra_ball_awarded = False
        game.shoot_again_manager = ShootAgainManager(
            game.event_bus,
            game.settings)
        game.event_bus.subscribe(
            BALL_DRAINED,
            game.on_ball_drained)
        game.event_bus.subscribe(
            BALL_LAUNCHED,
            game.on_ball_launched)
        game.event_bus.subscribe(
            EXTRA_BALL_AWARDED,
            game.on_extra_ball_awarded)
        game.event_bus.subscribe(
            BALL_READY,
            game.on_ball_ready)
        game.event_bus.subscribe(
            SWITCH_PRESSED,
            game.on_switch_pressed)
        return game


if __name__ == "__main__":
    unittest.main()
