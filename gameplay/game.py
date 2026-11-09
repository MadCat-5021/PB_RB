# gameplay/game_manager.py

from core.event_bus import EventBus
from core.state_manager import StateManager
from gameplay.target_manager import TargetManager
from gameplay.score_manager import ScoreManager
from input.input_manager import InputManager
from content.validator import validate

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

  def run(self):
        self.input_manager.run()
