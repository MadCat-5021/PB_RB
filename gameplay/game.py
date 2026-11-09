# gameplay/game.py

from core.event_bus import EventBus
from core.state_manager import StateManager

from gameplay.target_manager import TargetManager
from gameplay.score_manager import ScoreManager
from gameplay.groups import Group
from gameplay.sequences import Sequence

from input.input_manager import InputManager

from content.validator import validate
from content.groups import GROUPS
from content.sequences import SEQUENCES


class Game:
    def __init__(self):
        validate()

        self.event_bus = EventBus()

        self.state_manager = StateManager(
            self.event_bus
        )

        self.target_manager = TargetManager(
            self.event_bus
        )

        self.score_manager = ScoreManager(
            self.event_bus
        )

        self.input_manager = InputManager(
            self.event_bus
        )

        # Instantiate Groups
        self.groups = [
            Group(
                group["name"],
                group["targets"],
                self.event_bus,
                self.target_manager
            )
            for group in GROUPS
        ]

        # Instantiate Sequences
        self.sequences = [
            Sequence(
                sequence["name"],
                sequence["targets"],
                self.event_bus
            )
            for sequence in SEQUENCES
        ]

    def run(self):
        self.input_manager.run()