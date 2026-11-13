import unittest
from contextlib import redirect_stdout
from io import StringIO

from core.event_bus import EventBus
from core.events import GAME_ENDED, PRE_TURN, TURN_ENDED
from gameplay.game import Game
from gameplay.player_manager import PlayerManager


class Settings:
    def get(self, name):
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class GameTurnTests(unittest.TestCase):
    def test_pre_turn_prints_active_player_status(self):
        manager = PlayerManager(Settings())
        manager.start_game()
        manager.add_score(1250)
        manager.add_bonus(500)
        manager.complete_mission("MISSION_A")
        manager.set_challenge_progress("CHALLENGE_A", 1)

        game = Game.__new__(Game)
        game.player_manager = manager
        game.first_ball_of_turn = False
        game.first_ball_launched = True
        game.waiting_for_ball_launched = True

        output = StringIO()
        with redirect_stdout(output):
            game.on_pre_turn(PRE_TURN, {})

        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "PRE-TURN: PLAYER 1, BALL 1/3",
                "SCORE: 1250 | BONUS: 500",
                "MISSIONS: 1 completed | CHALLENGES: 0 completed"
            ])
        self.assertTrue(game.first_ball_of_turn)
        self.assertFalse(game.first_ball_launched)
        self.assertFalse(game.waiting_for_ball_launched)

    def test_players_rotate_through_configured_balls_then_game_ends(self):
        game = Game.__new__(Game)
        game.event_bus = EventBus()
        game.settings = Settings()
        game.player_manager = PlayerManager(game.settings)
        game.player_manager.start_game()
        game.player_manager.add_player()
        game.ball_launched = True
        game.game_active = True
        game.initial_ball_pending = False
        game.waiting_for_ball_launched = False
        game.event_bus.subscribe(PRE_TURN, game.on_pre_turn)
        game.event_bus.subscribe(TURN_ENDED, game.on_turn_ended)

        turns = []
        games_ended = []
        supplies = []
        game.event_bus.subscribe(
            PRE_TURN,
            lambda _event, data: turns.append(data))
        game.event_bus.subscribe(
            GAME_ENDED,
            lambda _event, data: games_ended.append(data))
        game.event_bus.subscribe(
            "BALL_SUPPLY",
            lambda *_: supplies.append(True))

        expected_turns = [
            (2, 1),
            (1, 2),
            (2, 2),
            (1, 3),
            (2, 3)
        ]
        with redirect_stdout(StringIO()):
            for expected_player, expected_ball in expected_turns:
                game.ball_launched = False
                game.event_bus.publish(TURN_ENDED, {})
                self.assertEqual(
                    (
                        game.player_manager.current_player.number,
                        game.player_manager.current_ball
                    ),
                    (expected_player, expected_ball))
                game.event_bus.publish(TURN_ENDED, {})

            game.ball_launched = False
            game.event_bus.publish(TURN_ENDED, {})

        self.assertEqual(len(games_ended), 1)
        result = games_ended[0]
        self.assertEqual(result["players"], 2)
        self.assertEqual(result["balls_per_game"], 3)
        self.assertEqual(result["balls_played"], [3, 3])
        self.assertEqual(
            [(turn["player"], turn["ball"]) for turn in turns],
            expected_turns)
        self.assertFalse(game.game_active)
        self.assertFalse(game.ball_launched)
        self.assertEqual(len(supplies), 5)


if __name__ == "__main__":
    unittest.main()
