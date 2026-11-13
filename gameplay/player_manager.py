from dataclasses import asdict, dataclass, field


@dataclass
class PlayerProgress:
    number: int
    score: int = 0
    bonus: int = 0
    balls_played: int = 0
    mission_progress: dict[str, int] = field(default_factory=dict)
    completed_missions: list[str] = field(default_factory=list)
    challenge_progress: dict[str, int] = field(default_factory=dict)
    completed_challenges: list[str] = field(default_factory=list)


class PlayerManager:

    def __init__(
        self,
        settings):
        self.settings = settings
        self.players: list[PlayerProgress] = []
        self.current_player_index = 0
        self.current_ball = 0
        self.balls_per_game = 0
        self.game_active = False

    @property
    def player_count(self):
        return len(self.players)

    @property
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.current_player_index]

    def start_game(self):
        balls_per_game = self.settings.get("BALLS_PER_GAME")
        if balls_per_game < 1:
            raise ValueError("BALLS_PER_GAME must be at least 1")
        self.players = [PlayerProgress(number=1)]
        self.current_player_index = 0
        self.current_ball = 1
        self.balls_per_game = balls_per_game
        self.game_active = True

    def add_player(self):
        if not self.game_active:
            raise RuntimeError("Cannot add a player before the game starts")
        if self.player_count >= self.settings.get("MAX_PLAYERS"):
            return False
        self.players.append(
            PlayerProgress(number=self.player_count + 1))
        return True

    def finish_turn(self):
        if not self.game_active or self.current_player is None:
            raise RuntimeError("Cannot finish a turn when no game is active")

        self.current_player.balls_played += 1

        for offset in range(1, self.player_count):
            next_index = (
                self.current_player_index + offset
            ) % self.player_count
            if self.players[next_index].balls_played < self.current_ball:
                self.current_player_index = next_index
                return None

        if self.current_ball >= self.balls_per_game:
            self.game_active = False
            return {
                "players": self.player_count,
                "balls_per_game": self.balls_per_game,
                "balls_played": [
                    player.balls_played
                    for player in self.players
                ],
                "results": self.get_results()
            }

        self.current_ball += 1
        self.current_player_index = 0
        return None

    def add_score(self, points):
        if not self.game_active or self.current_player is None:
            return False
        self.current_player.score += points
        return True

    def add_bonus(self, points):
        if not self.game_active or self.current_player is None:
            return False
        self.current_player.bonus += points
        return True

    def get_score(self, player_number=None):
        player = self._get_player_or_active(player_number)
        return 0 if player is None else player.score

    def get_bonus(self, player_number=None):
        player = self._get_player_or_active(player_number)
        return 0 if player is None else player.bonus

    def set_mission_progress(self, mission, progress):
        self._require_active_player().mission_progress[mission] = progress

    def complete_mission(self, mission):
        player = self._require_active_player()
        if mission not in player.completed_missions:
            player.completed_missions.append(mission)

    def set_challenge_progress(self, challenge, progress):
        self._require_active_player().challenge_progress[challenge] = progress

    def complete_challenge(self, challenge):
        player = self._require_active_player()
        if challenge not in player.completed_challenges:
            player.completed_challenges.append(challenge)

    def get_results(self):
        return [asdict(player) for player in self.players]

    def _get_player_or_active(self, player_number):
        if player_number is None:
            return self.current_player
        if player_number < 1 or player_number > self.player_count:
            raise ValueError(f"Unknown player number: {player_number}")
        return self.players[player_number - 1]

    def _require_active_player(self):
        if self.current_player is None:
            raise RuntimeError("No active player")
        return self.current_player
