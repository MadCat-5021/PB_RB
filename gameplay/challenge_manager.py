from random import random
from time import monotonic

from content.challenges import CHALLENGES
from core.events import (
    BALL_DRAINED,
    CHALLENGE_COMPLETED,
    CHALLENGE_FAILED,
    CHALLENGE_PROGRESS_UPDATED,
    CHALLENGE_STARTED,
    CHALLENGE_TIMER_EXPIRED,
    CHALLENGE_TIMER_STARTED,
    GROUP_COMPLETED,
    SEQUENCE_COMPLETED,
    SWITCH_PRESSED,
)


class ChallengeManager:
    def __init__(
        self,
        event_bus,
        player_manager,
        score_manager,
        target_manager,
    ):
        self.event_bus = event_bus
        self.player_manager = player_manager
        self.score_manager = score_manager
        self.target_manager = target_manager
        self.challenges = CHALLENGES
        self.active_challenge = None
        self.active_player_number = None
        self.deadline = None
        self.target_hits = {}
        self.completed_groups = set()
        self.completed_sequences = set()
        self.target_chain_index = 0

        self.event_bus.subscribe(SWITCH_PRESSED, self.on_target_hit)
        self.event_bus.subscribe(GROUP_COMPLETED, self.on_group_completed)
        self.event_bus.subscribe(
            SEQUENCE_COMPLETED,
            self.on_sequence_completed,
        )
        self.event_bus.subscribe(BALL_DRAINED, self.on_ball_drained)

    def on_target_hit(self, _event_type, data):
        switch = data["switch"]
        if switch == "DRAIN":
            return
        now = monotonic()
        was_active = self.active_challenge is not None
        self.update(now)
        if was_active:
            if self.active_challenge is not None:
                self._record_target_hit(switch)
            return

        player = self.player_manager.current_player
        if player is None or not self.player_manager.game_active:
            return

        for challenge in self.challenges:
            if (
                challenge["name"] in player.completed_challenges
                or not self._is_available(challenge, player)
                or not self._triggered_by_target_hit(challenge, switch)
            ):
                continue
            self._start(challenge, player, now)
            return

    def on_group_completed(self, _event_type, data):
        if self.active_challenge is None:
            return
        self.update()
        if self.active_challenge is None:
            return
        group = data["group"]
        if group not in self.active_challenge["requirements"]["groups"]:
            return
        if group not in self.completed_groups:
            self.completed_groups.add(group)
            self._update_progress_and_check_completion()

    def on_sequence_completed(self, _event_type, data):
        if self.active_challenge is None:
            return
        self.update()
        if self.active_challenge is None:
            return
        sequence = data["sequence"]
        if sequence not in self.active_challenge["requirements"]["sequences"]:
            return
        if sequence not in self.completed_sequences:
            self.completed_sequences.add(sequence)
            self._update_progress_and_check_completion()

    def on_ball_drained(self, _event_type, _data):
        if self.active_challenge is not None:
            self._fail("ball_drained")

    def update(self, now=None):
        if self.active_challenge is None or self.deadline is None:
            return
        now = monotonic() if now is None else now
        if now >= self.deadline:
            challenge = self.active_challenge
            challenge_name = challenge["name"]
            player_number = self.active_player_number
            self._print_failure(challenge, "timer_expired")
            self._clear_active()
            self.event_bus.publish(
                CHALLENGE_TIMER_EXPIRED,
                {
                    "challenge": challenge_name,
                    "player": player_number,
                },
            )
            self.event_bus.publish(
                CHALLENGE_FAILED,
                {
                    "challenge": challenge_name,
                    "player": player_number,
                    "reason": "timer_expired",
                },
            )

    def _is_available(self, challenge, player):
        missions = challenge["missions"]
        return not missions or player.active_mission in missions

    def _triggered_by_target_hit(self, challenge, target_name):
        trigger = challenge["trigger"]
        if trigger["type"] == "random":
            return random() < trigger["chance"]
        if trigger["type"] == "target_hit_multiple":
            if target_name != trigger["target"]:
                return False
            hit_count = self.target_manager.get_hit_count(target_name)
            return (
                hit_count % trigger["every"] == 0
                and random() < trigger["chance"]
            )
        return False

    def _start(self, challenge, player, now):
        self.active_challenge = challenge
        self.active_player_number = player.number
        self.deadline = (
            None
            if challenge["time_limit_seconds"] is None
            else now + challenge["time_limit_seconds"]
        )
        self.target_hits = [
            0 for _ in challenge["requirements"]["targets"]
        ]
        self.completed_groups = set()
        self.completed_sequences = set()
        self.target_chain_index = 0
        self.player_manager.set_challenge_progress(challenge["name"], 0)
        self._print_challenge_start(challenge)
        payload = {
            "challenge": challenge["name"],
            "player": player.number,
            "time_limit_seconds": challenge["time_limit_seconds"],
        }
        self.event_bus.publish(CHALLENGE_STARTED, payload)
        if self.deadline is not None:
            self.event_bus.publish(CHALLENGE_TIMER_STARTED, payload)

    @classmethod
    def _print_challenge_start(cls, challenge):
        print(f"CHALLENGE STARTED: {challenge['display_name']}")
        print(f"  {challenge['description']}")
        print("  REQUIREMENTS:")
        requirements = challenge["requirements"]
        for requirement in requirements["targets"]:
            target, hits = cls._target_requirement(requirement)
            print(f"    Target: {target} ({hits} hit(s))")
        for group in requirements["groups"]:
            print(f"    Group: {group}")
        for sequence in requirements["sequences"]:
            print(f"    Sequence: {sequence}")
        target_chain = challenge.get("target_chain", [])
        if target_chain:
            print(f"    Target chain: {' -> '.join(target_chain)}")

    def _record_target_hit(self, target_name):
        challenge = self.active_challenge
        requirements = challenge["requirements"]
        made_progress = False
        for index, requirement in enumerate(requirements["targets"]):
            name, required_hits = self._target_requirement(requirement)
            if target_name == name and self.target_hits[index] < required_hits:
                self.target_hits[index] += 1
                made_progress = True
                break

        target_chain = challenge.get("target_chain", [])
        if (
            self.target_chain_index < len(target_chain)
            and target_name == target_chain[self.target_chain_index]
        ):
            self.target_chain_index += 1
            made_progress = True
            if challenge.get("time_bonus_per_hit", 0) > 0:
                self.deadline += challenge["time_bonus_per_hit"]

        if made_progress:
            self._update_progress_and_check_completion()

    @staticmethod
    def _target_requirement(requirement):
        if isinstance(requirement, dict):
            return requirement["name"], requirement["hits"]
        return requirement, 1

    def _update_progress_and_check_completion(self):
        challenge = self.active_challenge
        if challenge is None:
            return

        requirements = challenge["requirements"]
        progress = (
            sum(self.target_hits)
            + len(self.completed_groups.intersection(requirements["groups"]))
            + len(
                self.completed_sequences.intersection(
                    requirements["sequences"]
                )
            )
            + self.target_chain_index
        )
        total = (
            sum(
                self._target_requirement(requirement)[1]
                for requirement in requirements["targets"]
            )
            + len(requirements["groups"])
            + len(requirements["sequences"])
            + len(challenge.get("target_chain", []))
        )
        self.player_manager.set_challenge_progress(
            challenge["name"],
            progress,
        )
        self.event_bus.publish(
            CHALLENGE_PROGRESS_UPDATED,
            {
                "challenge": challenge["name"],
                "player": self.active_player_number,
                "progress": progress,
                "required": total,
            },
        )
        if progress == total:
            self._complete()

    def _complete(self):
        challenge = self.active_challenge
        player_number = self.active_player_number
        self.player_manager.complete_challenge(
            challenge["name"],
            player_number,
        )
        self.score_manager.add_score(challenge["score"])
        print(
            f"CHALLENGE COMPLETED: {challenge['display_name']} "
            f"(+{challenge['score']} points)"
        )
        self._clear_active()
        self.event_bus.publish(
            CHALLENGE_COMPLETED,
            {
                "challenge": challenge["name"],
                "player": player_number,
                "score": challenge["score"],
            },
        )

    def _fail(self, reason):
        challenge = self.active_challenge
        if challenge is None:
            return
        player_number = self.active_player_number
        self._print_failure(challenge, reason)
        self._clear_active()
        self.event_bus.publish(
            CHALLENGE_FAILED,
            {
                "challenge": challenge["name"],
                "player": player_number,
                "reason": reason,
            },
        )

    @staticmethod
    def _print_failure(challenge, reason):
        reason_text = {
            "timer_expired": "time expired",
            "ball_drained": "ball drained",
        }.get(reason, reason.replace("_", " "))
        print(
            f"CHALLENGE FAILED: {challenge['display_name']} "
            f"({reason_text})"
        )

    def _clear_active(self):
        self.active_challenge = None
        self.active_player_number = None
        self.deadline = None
        self.target_hits = []
        self.completed_groups = set()
        self.completed_sequences = set()
        self.target_chain_index = 0
