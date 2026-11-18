import copy
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from content.challenges import CHALLENGES
from core.event_bus import EventBus
from core.events import (
    CHALLENGE_COMPLETED,
    CHALLENGE_FAILED,
    CHALLENGE_PROGRESS_UPDATED,
    CHALLENGE_TIMER_EXPIRED,
    GROUP_COMPLETED,
    SEQUENCE_COMPLETED,
    SWITCH_PRESSED,
)
from gameplay.challenge_manager import ChallengeManager
from gameplay.player_manager import PlayerManager
from gameplay.score_manager import ScoreManager
from gameplay.target_manager import TargetManager


class Settings:
    def get(self, name):
        if name == "BALLS_PER_GAME":
            return 3
        if name == "MAX_PLAYERS":
            return 4
        raise KeyError(name)


class ChallengeManagerTests(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        self.player_manager = PlayerManager(Settings())
        self.player_manager.start_game()
        self.score_manager = ScoreManager(
            self.event_bus,
            self.player_manager,
        )
        self.target_manager = TargetManager(self.event_bus)
        self.events = {
            CHALLENGE_COMPLETED: [],
            CHALLENGE_FAILED: [],
            CHALLENGE_PROGRESS_UPDATED: [],
            CHALLENGE_TIMER_EXPIRED: [],
        }
        for event_type, events in self.events.items():
            self.event_bus.subscribe(
                event_type,
                lambda _event, data, events=events: events.append(data),
            )

    def make_manager(self, challenge):
        with patch(
            "gameplay.challenge_manager.CHALLENGES",
            [challenge],
        ):
            return ChallengeManager(
                self.event_bus,
                self.player_manager,
                self.score_manager,
                self.target_manager,
            )

    def test_target_chain_ignores_other_hits_and_awards_time_bonus(self):
        challenge = copy.deepcopy(
            next(
                challenge
                for challenge in CHALLENGES
                if challenge["name"] == "TRACK_ATTACK_CHAIN"
            )
        )
        manager = self.make_manager(challenge)

        output = StringIO()
        with redirect_stdout(output):
            with patch("gameplay.challenge_manager.random", return_value=0):
                with patch(
                    "gameplay.challenge_manager.monotonic",
                    return_value=100,
                ):
                    self.event_bus.publish(
                        SWITCH_PRESSED,
                        {"switch": "GENERAL_FILLER_1"},
                    )
                    self.event_bus.publish(
                        SWITCH_PRESSED,
                        {"switch": "RAMP_LEFT"},
                    )
                    self.assertEqual(manager.target_chain_index, 0)
                    self.assertEqual(
                        self.events[CHALLENGE_PROGRESS_UPDATED],
                        [],
                    )

                    for target in challenge["target_chain"]:
                        self.event_bus.publish(
                            SWITCH_PRESSED,
                            {"switch": target},
                        )

        self.assertIsNone(manager.active_challenge)
        self.assertEqual(manager.deadline, None)
        self.assertIn(
            "CHALLENGE STARTED: Safety car",
            output.getvalue(),
        )
        self.assertIn(
            "Follow the safety car, stay within 10 car lengths",
            output.getvalue(),
        )
        self.assertIn(
            "Target chain: ORBIT_LEFT_FRONT -> RAMP_LEFT -> "
            "SWITCHBACK_ENTRY -> ORBIT_RIGHT_REAR",
            output.getvalue(),
        )
        self.assertIn("CHALLENGE COMPLETED: Safety car", output.getvalue())
        self.assertEqual(
            self.events[CHALLENGE_COMPLETED],
            [{
                "challenge": "TRACK_ATTACK_CHAIN",
                "player": 1,
                "score": 50000,
            }],
        )
        self.assertEqual(self.score_manager.get_score(), 50080)
        self.assertEqual(
            self.player_manager.current_player.completed_challenges,
            ["TRACK_ATTACK_CHAIN"],
        )

    def test_challenge_completes_when_target_group_and_sequence_requirements_pass(self):
        challenge = copy.deepcopy(CHALLENGES[0])
        challenge["trigger"] = {
            "type": "random",
            "check_on": "target_hit",
            "chance": 1.0,
        }
        challenge["requirements"]["targets"] = [
            {"name": "POP_1", "hits": 2},
        ]
        challenge["requirements"]["groups"] = ["TIRE"]
        challenge["requirements"]["sequences"] = ["SWITCHBACK"]
        manager = self.make_manager(challenge)

        output = StringIO()
        with redirect_stdout(output):
            with patch("gameplay.challenge_manager.random", return_value=0):
                with patch(
                    "gameplay.challenge_manager.monotonic",
                    return_value=100,
                ):
                    self.event_bus.publish(
                        SWITCH_PRESSED,
                        {"switch": "GENERAL_FILLER_1"},
                    )
                    for _ in range(2):
                        self.event_bus.publish(
                            SWITCH_PRESSED,
                            {"switch": "POP_1"},
                        )
                    self.event_bus.publish(
                        GROUP_COMPLETED,
                        {"group": "TIRE"},
                    )
                    self.event_bus.publish(
                        SEQUENCE_COMPLETED,
                        {"sequence": "SWITCHBACK"},
                    )

        self.assertIsNone(manager.active_challenge)
        self.assertEqual(len(self.events[CHALLENGE_COMPLETED]), 1)
        self.assertIn("Target: POP_1 (2 hit(s))", output.getvalue())
        self.assertIn("Group: TIRE", output.getvalue())
        self.assertIn("Sequence: SWITCHBACK", output.getvalue())

    def test_timer_expiry_fails_challenge(self):
        challenge = copy.deepcopy(CHALLENGES[0])
        challenge["trigger"] = {
            "type": "random",
            "check_on": "target_hit",
            "chance": 1.0,
        }
        manager = self.make_manager(challenge)

        with patch("gameplay.challenge_manager.random", return_value=0):
            with patch("gameplay.challenge_manager.monotonic", return_value=100):
                self.event_bus.publish(
                    SWITCH_PRESSED,
                    {"switch": "GENERAL_FILLER_1"},
                )

        output = StringIO()
        with redirect_stdout(output):
            manager.update(now=160)

        self.assertIn(
            "CHALLENGE FAILED: Pitstop Dash (time expired)",
            output.getvalue(),
        )
        self.assertEqual(
            self.events[CHALLENGE_TIMER_EXPIRED],
            [{"challenge": challenge["name"], "player": 1}],
        )
        self.assertEqual(
            self.events[CHALLENGE_FAILED],
            [{
                "challenge": challenge["name"],
                "player": 1,
                "reason": "timer_expired",
            }],
        )
        self.assertIsNone(manager.active_challenge)


if __name__ == "__main__":
    unittest.main()
