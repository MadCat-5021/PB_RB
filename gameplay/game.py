# gameplay/game.py

from time import monotonic, sleep, time
from core.event_bus import EventBus
from core.events import (
    BALL_DRAINED,
    BALL_LAUNCHED,
    BALL_READY,
    BALL_STARTED,
    BALL_SUPPLY,
    EXTRA_BALL_AWARDED,
    GAME_LAUNCH_REQUESTED,
    GAME_ENDED,
    HIGHSCORES,
    LAUNCH_SEQUENCE,
    PRE_TURN,
    SHOOT_AGAIN_STARTED,
    START_REQUESTED,
    SWITCH_PRESSED,
    SWITCH_RELEASED,
    TURN_ENDED
)
from core.state_manager import StateManager
from core.settings_manager import SettingsManager
from gameplay.ball_manager import BallManager
from gameplay.control_manager import ControlManager
from gameplay.launch_manager import LaunchManager
from gameplay.player_manager import PlayerManager
from gameplay.shoot_again_manager import ShootAgainManager
from gameplay.target_manager import TargetManager
from gameplay.score_manager import ScoreManager
from gameplay.groups import Group
from gameplay.sequences import Sequence
from hardware.coil_manager import CoilManager
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
        self.player_manager = PlayerManager(self.settings)
        self.ball_launched = False
        self.game_active = False
        self.game_started_at = 0
        self.initial_ball_pending = False
        self.first_ball_of_turn = False
        self.first_ball_launched = False
        self.waiting_for_ball_launched = False
        self.extra_ball_awarded = False
        self.game_end_stage = None
        self.game_end_deadline = None
        self.event_bus.subscribe(GAME_LAUNCH_REQUESTED,self.on_game_launch_requested)
        self.event_bus.subscribe(START_REQUESTED,self.on_start_requested)
        self.event_bus.subscribe(GAME_ENDED,self.on_game_ended)
        self.event_bus.subscribe(BALL_READY,self.on_ball_ready)
        self.event_bus.subscribe(BALL_LAUNCHED,self.on_ball_launched)
        self.event_bus.subscribe(BALL_DRAINED,self.on_ball_drained)
        self.event_bus.subscribe(EXTRA_BALL_AWARDED,self.on_extra_ball_awarded)
        self.event_bus.subscribe(TURN_ENDED,self.on_turn_ended)
        self.event_bus.subscribe(PRE_TURN,self.on_pre_turn)
        self.event_bus.subscribe(SWITCH_PRESSED,self.on_switch_pressed)
        self.event_bus.subscribe(SWITCH_RELEASED,self.on_switch_released)
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
            self.event_bus,
            self.player_manager)
        self.input_manager = InputManager(
            self.event_bus)
        self.coil_manager = CoilManager()
        self.ball_manager = BallManager(
            self.event_bus,
            self.coil_manager,
            self.target_manager,
            self.settings)
        self.launch_manager = LaunchManager(self.event_bus)
        self.shoot_again_manager = ShootAgainManager(
            self.event_bus,
            self.settings)
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

    def on_game_ended(
        self,
        _event_type,
        data):
        print("GAME OVER")
        for player in data["results"]:
            print(
                f"PLAYER {player['number']} FINAL SCORE: "
                f"{player['score']} | BONUS: {player['bonus']}"
            )

        self.game_end_stage = "highscores"
        self.game_end_deadline = monotonic() + 2

    def update_game_end(self):
        if self.game_end_stage is None:
            return
        if monotonic() < self.game_end_deadline:
            return

        if self.game_end_stage == "highscores":
            self.state_manager.set_state("HIGHSCORE")
            self.event_bus.publish(
                HIGHSCORES,
                {"results": self.player_manager.get_results()})
            print("HIGHSCORE SCREEN")
            self.game_end_stage = "active"
            self.game_end_deadline = monotonic() + 2
            return

        if self.game_end_stage == "active":
            self.state_manager.set_state("ACTIVE")
            self.game_end_stage = None
            self.game_end_deadline = None
        
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
            self.player_manager.start_game()
            self.game_active = True
            self.ball_launched = False
            self.initial_ball_pending = True
            self.extra_ball_awarded = False
            self.game_started_at = time()
            if not freeplay:
                self.control_manager.credits -= 1
            self.event_bus.publish(
                PRE_TURN,
                {})
            print("GAME STARTED")
            print(f"PLAYERS: {self.player_manager.player_count}")
            self.state_manager.set_state(
                "GAME")
            return
        if self.ball_launched:
            print(
                "ADD PLAYER DENIED: BALL IN PLAY")
            return
        if self.player_manager.player_count >= self.settings.get("MAX_PLAYERS"):
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
        if not self.player_manager.add_player():
            print("ADD PLAYER DENIED: MAX PLAYERS")
            return
        print(f"PLAYER {self.player_manager.player_count} ADDED")

    def run(self):
        self.input_manager.run()
        while True:
            self.state_manager.check_timeouts()
            self.update_game_end()
            self.launch_manager.update()
            self.shoot_again_manager.update()
            self.check_game_start()
            self.ball_manager.check_supply()
            sleep(0.1)

    def check_game_start(self):
        if not self.game_active:
            return
        if not self.initial_ball_pending:
            return
        if self.ball_launched:
            return
        if (time() - self.game_started_at < self.settings.get("GAME_START_TIMEOUT")):
            return
        self.supply_ball()

    def supply_ball(self):
        print("BALL SUPPLY")
        self.initial_ball_pending = False
        self.event_bus.publish(
            BALL_SUPPLY,
            {})
        self.ball_launched = True

    def on_ball_ready(
        self,
        _event_type,
        _data):
        print("BALL READY RECEIVED")
        self.waiting_for_ball_launched = True
        print("WAITING FOR BALL LAUNCHED")
        if not self.first_ball_of_turn:
            return
        self.first_ball_of_turn = False
        if self.settings.get("MACHINE_HAS_LAUNCH_SEQUENCE"):
            self.event_bus.publish(
                LAUNCH_SEQUENCE,
                {})

    def on_pre_turn(
        self,
        _event_type,
        _data):
        self.first_ball_of_turn = True
        self.first_ball_launched = False
        self.waiting_for_ball_launched = False
        player = self.player_manager.current_player
        if player is None:
            return
        print(
            f"PRE-TURN: PLAYER {player.number}, "
            f"BALL {self.player_manager.current_ball}/"
            f"{self.player_manager.balls_per_game}"
        )
        print(f"SCORE: {player.score} | BONUS: {player.bonus}")
        print(
            f"MISSIONS: {len(player.completed_missions)} completed | "
            f"CHALLENGES: {len(player.completed_challenges)} completed"
        )

    def on_switch_released(
        self,
        _event_type,
        data):
        if not self.waiting_for_ball_launched:
            return
        if data["switch"] != "PLUNGER":
            return
        self.event_bus.publish(
            BALL_LAUNCHED,
            {})

    def on_switch_pressed(
        self,
        _event_type,
        data):
        if data["switch"] != "DRAIN":
            return
        self.event_bus.publish(BALL_DRAINED, {})

    def on_ball_launched(
        self,
        _event_type,
        _data):
        if not self.waiting_for_ball_launched:
            print("BALL LAUNCHED IGNORED: NOT WAITING FOR A BALL")
            return
        self.waiting_for_ball_launched = False
        first_ball = not self.first_ball_launched
        self.first_ball_launched = True
        print("BALL STARTED")
        self.event_bus.publish(
            BALL_STARTED,
            {})
        if first_ball:
            self.event_bus.publish(
                SHOOT_AGAIN_STARTED,
                {})

    def on_extra_ball_awarded(
        self,
        _event_type,
        _data):
        self.extra_ball_awarded = True

    def on_ball_drained(
        self,
        _event_type,
        _data):
        if not self.game_active or not self.ball_launched:
            return

        self.ball_launched = False
        self.waiting_for_ball_launched = False

        if self.shoot_again_manager.is_active():
            self.shoot_again_manager.deactivate()
            self.first_ball_of_turn = False
            self.supply_ball()
            return

        if self.extra_ball_awarded:
            self.extra_ball_awarded = False
            self.first_ball_of_turn = False
            self.supply_ball()
            return

        self.event_bus.publish(TURN_ENDED, {})

    def on_turn_ended(
        self,
        _event_type,
        _data):
        if not self.game_active or self.ball_launched:
            return

        game_result = self.player_manager.finish_turn()
        if game_result is not None:
            self.game_active = False
            self.initial_ball_pending = False
            self.waiting_for_ball_launched = False
            self.event_bus.publish(GAME_ENDED, game_result)
            return

        self.event_bus.publish(
            PRE_TURN,
            {
                "player": self.player_manager.current_player.number,
                "ball": self.player_manager.current_ball
            })
        self.supply_ball()