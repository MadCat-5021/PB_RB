import unittest

from gameplay.player_manager import PlayerManager


class Settings:
    def get(self, name):
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class PlayerManagerTests(unittest.TestCase):
    def test_player_score_bonus_and_progress_are_independent(self):
        manager = PlayerManager(Settings())
        manager.start_game()
        manager.add_player()

        manager.add_score(100)
        manager.add_bonus(50)
        manager.set_mission_progress("MISSION_A", 2)
        manager.complete_mission("MISSION_A")
        manager.set_challenge_progress("CHALLENGE_A", 1)
        manager.complete_challenge("CHALLENGE_A")

        manager.current_player_index = 1
        manager.add_score(200)
        manager.add_bonus(25)
        manager.set_mission_progress("MISSION_A", 1)

        self.assertEqual(manager.get_score(1), 100)
        self.assertEqual(manager.get_bonus(1), 50)
        self.assertEqual(manager.get_score(2), 200)
        self.assertEqual(manager.get_bonus(2), 25)
        results = manager.get_results()
        self.assertEqual(results[0]["mission_progress"], {"MISSION_A": 2})
        self.assertEqual(results[0]["completed_missions"], ["MISSION_A"])
        self.assertEqual(results[0]["challenge_progress"], {"CHALLENGE_A": 1})
        self.assertEqual(results[0]["completed_challenges"], ["CHALLENGE_A"])
        self.assertEqual(results[1]["mission_progress"], {"MISSION_A": 1})
        self.assertEqual(results[1]["completed_missions"], [])

    def test_game_results_include_each_players_final_totals(self):
        manager = PlayerManager(Settings())
        manager.start_game()
        manager.add_player()
        manager.add_score(300)
        manager.current_player_index = 1
        manager.add_score(150)

        result = None
        for _ in range(3):
            result = manager.finish_turn()
            if result is None:
                result = manager.finish_turn()

        self.assertEqual(result["players"], 2)
        self.assertEqual(
            [(player["number"], player["score"]) for player in result["results"]],
            [(1, 300), (2, 150)])
        self.assertEqual(result["balls_played"], [3, 3])

    def test_invalid_ball_count_is_rejected(self):
        class InvalidSettings:
            def get(self, name):
                if name == "BALLS_PER_GAME":
                    return 0
                raise KeyError(name)

        with self.assertRaises(ValueError):
            PlayerManager(InvalidSettings()).start_game()


if __name__ == "__main__":
    unittest.main()
