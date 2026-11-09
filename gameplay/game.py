# gameplay/game.py

from time import sleep

from core.event_bus import EventBus
from core.state_manager import StateManager
from core.settings_manager import SettingsManager

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
        self.event_bus = EventBus()
        self.settings = SettingsManager()

        self.state_manager = StateManager(
            self.event_bus,
            self.settings,
            "BOOT")

        self.boot()

    def boot(self):
        print("BOOT: Validating content...")
        validate()

        print("BOOT: Initializing managers...")
        self.target_manager = TargetManager(
            self.event_bus)

        self.score_manager = ScoreManager(
            self.event_bus)

        self.input_manager = InputManager(
            self.event_bus)

        print("BOOT: Loading groups...")
        self.groups = [
            Group(
                group["name"],
                group["targets"],
                self.event_bus,
                self.target_manager)
            for group in GROUPS]

        print("BOOT: Loading sequences...")
        self.sequences = [
            Sequence(
                sequence["name"],
                sequence["targets"],
                self.event_bus)
            for sequence in SEQUENCES]

        print("BOOT: Checking service mode...")

        if self.settings.get(
            "BOOT_SERVICE_MODE"):
            self.state_manager.set_state(
                "SERVICE_MODE")
        else:
            self.state_manager.set_state(
                "ACTIVE")

    def run(self):
        self.input_manager.run()

        while True:
            self.state_manager.check_timeouts()
            sleep(0.1)