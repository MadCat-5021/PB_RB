import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import call, patch

from core.event_bus import EventBus
from core.events import GAME_ENDED, HIGHSCORES, STATE_CHANGED
from core.state_manager import StateManager
from gameplay.game import Game


class Settings:
    pass


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

        with patch("gameplay.game.sleep") as sleep:
            with redirect_stdout(output):
                event_bus.publish(GAME_ENDED, result)

        self.assertIn("GAME OVER", output.getvalue())
        self.assertIn("PLAYER 1 FINAL SCORE: 12000 | BONUS: 500", output.getvalue())
        self.assertIn("HIGHSCORE SCREEN", output.getvalue())
        self.assertEqual(sleep.call_args_list, [call(2), call(2)])
        self.assertEqual(highscore_states, ["HIGHSCORE"])
        self.assertEqual(state_transitions, ["HIGHSCORE", "ACTIVE"])
        self.assertEqual(state_manager.get_state(), "ACTIVE")


if __name__ == "__main__":
    unittest.main()
