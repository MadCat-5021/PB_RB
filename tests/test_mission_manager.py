import unittest
from contextlib import redirect_stdout
from io import StringIO

from core.event_bus import EventBus
from core.events import (
    MISSION_COMPLETED,
    MISSION_STARTED,
    SEQUENCE_COMPLETED,
)
from gameplay.mission_manager import MissionManager
from gameplay.player_manager import PlayerManager
from gameplay.score_manager import ScoreManager


class Settings:
    def get(self, name):
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class MissionManagerTests(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        self.player_manager = PlayerManager(Settings())
        self.player_manager.start_game()
        self.player_manager.add_player()
        self.score_manager = ScoreManager(
            self.event_bus,
            self.player_manager)
        self.mission_manager = MissionManager(
            self.event_bus,
            self.player_manager,
            self.score_manager)

    def test_players_start_with_the_first_mission(self):
        self.assertEqual(
            [player.active_mission for player in self.player_manager.players],
            ["MISSION_1", "MISSION_1"])

    def test_completing_a_mission_starts_the_next_for_that_player(self):
        completed = []
        started = []
        self.event_bus.subscribe(
            MISSION_COMPLETED,
            lambda _event, data: completed.append(data))
        self.event_bus.subscribe(
            MISSION_STARTED,
            lambda _event, data: started.append(data))

        output = StringIO()
        with redirect_stdout(output):
            self.event_bus.publish(
                SEQUENCE_COMPLETED,
                {"sequence": "RAMP_RIGHT"})
            self.assertEqual(
                self.player_manager.current_player.active_mission,
                "MISSION_1")

            self.event_bus.publish(
                SEQUENCE_COMPLETED,
                {"sequence": "ORBIT_LONG"})

        self.assertEqual(
            self.player_manager.current_player.active_mission,
            "MISSION_2")
        self.assertEqual(
            self.player_manager.current_player.completed_missions,
            ["MISSION_1"])
        self.assertEqual(self.player_manager.get_score(), 7250)
        self.assertIn(
            "MISSION ACTIVE: MISSION_2 - Eau Rouge",
            output.getvalue())
        self.assertEqual(
            completed,
            [{"mission": "MISSION_1", "player": 1}])
        self.assertEqual(
            started,
            [{"mission": "MISSION_2", "player": 1}])
        self.assertEqual(
            self.player_manager.players[1].active_mission,
            "MISSION_1")


if __name__ == "__main__":
    unittest.main()
