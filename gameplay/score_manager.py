# gameplay/scoremanager.py

from core.events import (
    SWITCH_PRESSED,
    GROUP_COMPLETED,
    SEQUENCE_COMPLETED,
    LAUNCH_BONUS_AWARDED
)

from content.targets import TARGETS
from content.groups import GROUPS
from content.sequences import SEQUENCES


class ScoreManager:

    def __init__(self, event_bus, player_manager):

        self.event_bus = event_bus
        self.player_manager = player_manager

        self.targets = {
            target["name"]: target
            for target in TARGETS
        }

        self.groups = {
            group["name"]: group
            for group in GROUPS
        }

        self.sequences = {
            sequence["name"]: sequence
            for sequence in SEQUENCES
        }

        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

        self.event_bus.subscribe(
            GROUP_COMPLETED,
            self.on_group_completed
        )

        self.event_bus.subscribe(
            SEQUENCE_COMPLETED,
            self.on_sequence_completed
        )

        self.event_bus.subscribe(
            LAUNCH_BONUS_AWARDED,
            self.on_launch_bonus_awarded
        )

    def add_score(self, points):
        if not self.player_manager.add_score(points):
            print("SCORE IGNORED: NO ACTIVE PLAYER")
            return

        print(
            f"SCORE: +{points} "
            f"(PLAYER {self.player_manager.current_player.number}: "
            f"{self.player_manager.get_score()})"
        )

    def on_switch_pressed(
        self,
        _event_type,
        data
    ):

        target_name = data["switch"]

        if target_name not in self.targets:
            return

        score = self.targets[target_name]["score"]

        if score > 0:
            self.add_score(score)

    def on_group_completed(
        self,
        _event_type,
        data
    ):

        group_name = data["group"]

        if group_name not in self.groups:
            return

        self.add_score(
            self.groups[group_name]["score"]
        )

    def on_sequence_completed(
        self,
        _event_type,
        data
    ):

        sequence_name = data["sequence"]

        if sequence_name not in self.sequences:
            return

        self.add_score(
            self.sequences[sequence_name]["score"]
        )

    def get_score(self, player_number=None):
        return self.player_manager.get_score(player_number)

    def add_bonus(self, points):
        if not self.player_manager.add_bonus(points):
            print("BONUS IGNORED: NO ACTIVE PLAYER")
            return

        print(
            f"BONUS: +{points} "
            f"(PLAYER {self.player_manager.current_player.number}: "
            f"{self.player_manager.get_bonus()})"
        )

    def on_launch_bonus_awarded(
        self,
        _event_type,
        data
    ):

        self.add_bonus(data["points"])

    def get_bonus(self, player_number=None):
        return self.player_manager.get_bonus(player_number)