from core.events import (
    SWITCH_PRESSED,
    GROUP_COMPLETED,
    SEQUENCE_COMPLETED
)

from content.targets import TARGETS
from content.groups import GROUPS
from content.sequences import SEQUENCES


class ScoreManager:

    def __init__(self, event_bus):

        self.event_bus = event_bus

        self.score = 0

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

    def add_score(self, points):

        self.score += points

        print(
            f"SCORE: +{points} "
            f"(TOTAL: {self.score})"
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

    def get_score(self):

        return self.score