import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from core.event_bus import EventBus
from core.events import GAME_ENDED, HIGHSCORES, STATE_CHANGED
from core.state_manager import StateManager
from gameplay.game import Game
from gameplay.player_manager import PlayerManager


class Settings:
    def get(self, name):
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class GameEndTests(unittest.TestCase):
    def test_game_end_shows_scores_runs_highscores_then_returns_active(self):
        event_bus = EventBus()
        state_manager = StateManager(
            event_bus,
            Settings(),
            initial_state="GAME")
        game = Game.__new__(Game)
        game.event_bus = event_bus
        game.state_manager = state_manager
        game.player_manager = PlayerManager(Settings())
        game.player_manager.start_game()
        game.player_manager.add_score(12000)
        game.player_manager.add_bonus(500)
        game.game_end_stage = None
        game.game_end_deadline = None
        event_bus.subscribe(GAME_ENDED, game.on_game_ended)

        highscore_states = []
        state_transitions = []
        event_bus.subscribe(
            HIGHSCORES,
            lambda _event, _data: highscore_states.append(
                state_manager.get_state()))
        event_bus.subscribe(
            STATE_CHANGED,
            lambda _event, data: state_transitions.append(
                data["new_state"]))
        result = {
            "results": [
                {"number": 1, "score": 12000, "bonus": 500}
            ]
        }
        output = StringIO()

        with patch(
            "gameplay.game.monotonic",
            side_effect=[10, 11, 12, 13, 14, 15]
        ):
            with redirect_stdout(output):
                event_bus.publish(GAME_ENDED, result)
                self.assertEqual(state_manager.get_state(), "GAME")
                game.update_game_end()
                self.assertEqual(state_manager.get_state(), "GAME")
                game.update_game_end()
                self.assertEqual(state_manager.get_state(), "HIGHSCORE")
                game.update_game_end()
                self.assertEqual(state_manager.get_state(), "HIGHSCORE")
                game.update_game_end()

        self.assertIn("GAME OVER", output.getvalue())
        self.assertIn("PLAYER 1 FINAL SCORE: 12000 | BONUS: 500", output.getvalue())
        self.assertIn("HIGHSCORE SCREEN", output.getvalue())
        self.assertEqual(highscore_states, ["HIGHSCORE"])
        self.assertEqual(state_transitions, ["HIGHSCORE", "ACTIVE"])
        self.assertEqual(state_manager.get_state(), "ACTIVE")

    def test_completed_game_does_not_accept_late_score_awards(self):
        player_manager = PlayerManager(Settings())
        player_manager.start_game()
        player_manager.add_score(100)
        player_manager.game_active = False

        self.assertFalse(player_manager.add_score(50))
        self.assertFalse(player_manager.add_bonus(25))
        self.assertEqual(player_manager.get_score(), 100)
        self.assertEqual(player_manager.get_bonus(), 0)


if __name__ == "__main__":
    unittest.main()
