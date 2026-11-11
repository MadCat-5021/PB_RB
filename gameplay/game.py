# gameplay/game.py

from time import sleep, time
from core.event_bus import EventBus
from core.events import (START_REQUESTED,GAME_LAUNCH_REQUESTED,BALL_SUPPLY,BALL_READY,PRE_TURN)
from core.state_manager import StateManager
from core.settings_manager import SettingsManager
from gameplay.control_manager import ControlManager
from gameplay.target_manager import TargetManager
from gameplay.score_manager import ScoreManager
from gameplay.groups import Group
from gameplay.sequences import Sequence
from input.input_manager import InputManager
from content.validator import validate
from content.groups import GROUPS
from content.sequences import SEQUENCES
from gameplay.ball_manager import BallManager

class Game:
    def __init__(self):
        self.event_bus = EventBus()
        self.settings = SettingsManager()
        self.state_manager = StateManager(
            self.event_bus,
            self.settings,
            "BOOT")
        self.players = 0
        self.ball_launched = False
        self.game_active = False
        self.game_started_at = 0
        self.event_bus.subscribe(GAME_LAUNCH_REQUESTED,self.on_game_launch_requested)
        self.event_bus.subscribe(START_REQUESTED,self.on_start_requested)
        self.event_bus.subscribe(BALL_READY,self.on_ball_ready)
        self.boot()

    def boot(self):
        print("BOOT: Validating content...")
        validate()
        print("BOOT: Initializing managers...")
        self.control_manager = ControlManager(
            self.event_bus)
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
        if self.settings.get("BOOT_SERVICE_MODE"):
            self.state_manager.set_state("SERVICE_MODE")
        else:
            self.state_manager.set_state("ACTIVE")

    def on_game_launch_requested(
        self,
        event_type,
        data):
        if not self.game_active:
            return
        if self.ball_launched:
            return
        self.supply_ball()
        
    def on_start_requested(
        self,
        event_type,
        data):
        print("START REQUEST RECEIVED")

        credits = self.control_manager.get_credits()
        freeplay = self.settings.get("FREEPLAY")

        if not self.game_active:
            if (
                not freeplay
                and credits <= 0
            ):
                print("START DENIED: NO CREDITS")
                return

            self.game_active = True
            self.players = 1
            self.ball_launched = False
            self.game_started_at = time()

            if not freeplay:
                self.control_manager.credits -= 1

            self.event_bus.publish(
                PRE_TURN,
                {})

            print("GAME STARTED")
            print(f"PLAYERS: {self.players}")

            self.state_manager.set_state(
                "GAME")

            return

        if self.ball_launched:
            print(
                "ADD PLAYER DENIED: BALL IN PLAY")
            return

        if self.players >= 4:
            print(
                "ADD PLAYER DENIED: MAX PLAYERS")
            return

        if (
            not freeplay
            and credits <= 0
        ):
            print(
                "ADD PLAYER DENIED: NO CREDITS")
            return

        if not freeplay:
            self.control_manager.credits -= 1

        self.players += 1

        print(
            f"PLAYER {self.players} ADDED")

    def run(self):
        self.input_manager.run()
        while True:
            self.state_manager.check_timeouts()
            self.check_game_start()
            sleep(0.1)

    def check_game_start(self):
        if not self.game_active:
            return
        if self.ball_launched:
            return
        if (time() - self.game_started_at < self.settings.get("GAME_START_TIMEOUT")):
            return
        self.supply_ball()

    def supply_ball(self):
        print("BALL SUPPLY")
        self.event_bus.publish(
            BALL_SUPPLY,
            {})
        self.ball_launched = True

    def on_ball_ready(
        self,
        event_type,
        data):
        print("BALL READY RECEIVED")        