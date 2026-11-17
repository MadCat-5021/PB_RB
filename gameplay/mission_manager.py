from content.missions import MISSIONS
from core.events import (
    GROUP_COMPLETED,
    MISSION_COMPLETED,
    MISSION_PROGRESS_UPDATED,
    MISSION_STARTED,
    SEQUENCE_COMPLETED,
    SWITCH_PRESSED,
)


class MissionManager:
    def __init__(self, event_bus, player_manager, score_manager):
        self.event_bus = event_bus
        self.player_manager = player_manager
        self.score_manager = score_manager
        self.missions = MISSIONS
        self.missions_by_name = {
            mission["name"]: mission
            for mission in self.missions
        }

        self.event_bus.subscribe(SWITCH_PRESSED, self.on_target_hit)
        self.event_bus.subscribe(GROUP_COMPLETED, self.on_group_completed)
        self.event_bus.subscribe(
            SEQUENCE_COMPLETED,
            self.on_sequence_completed)

    def get_mission(self, mission_name):
        if mission_name is None:
            return None
        return self.missions_by_name[mission_name]

    def start_player_mission(self, player):
        if player.active_mission is None:
            return
        self.event_bus.publish(
            MISSION_STARTED,
            {
                "mission": player.active_mission,
                "player": player.number,
            })

    def on_target_hit(self, _event_type, data):
        self._record_requirement("targets", data["switch"])

    def on_group_completed(self, _event_type, data):
        self._record_requirement("groups", data["group"])

    def on_sequence_completed(self, _event_type, data):
        self._record_requirement("sequences", data["sequence"])

    def _record_requirement(self, requirement_type, requirement_name):
        player = self.player_manager.current_player
        if player is None or player.active_mission is None:
            return

        mission = self.get_mission(player.active_mission)
        if requirement_name not in mission["requirements"][requirement_type]:
            return

        completed = player.mission_requirements.setdefault(
            mission["name"],
            [])
        requirement = f"{requirement_type}:{requirement_name}"
        if requirement in completed:
            return

        completed.append(requirement)
        required = [
            f"{kind}:{name}"
            for kind, names in mission["requirements"].items()
            for name in names
        ]
        progress = len(completed)
        self.player_manager.set_mission_progress(
            mission["name"],
            progress)
        self.event_bus.publish(
            MISSION_PROGRESS_UPDATED,
            {
                "mission": mission["name"],
                "player": player.number,
                "progress": progress,
                "required": len(required),
            })

        if required and all(item in completed for item in required):
            self._complete_mission(player, mission)

    def _complete_mission(self, player, mission):
        self.player_manager.complete_mission(mission["name"])
        self.score_manager.add_score(mission["score"])
        self.event_bus.publish(
            MISSION_COMPLETED,
            {
                "mission": mission["name"],
                "player": player.number,
            })

        mission_index = self.missions.index(mission)
        next_index = mission_index + 1
        player.active_mission = (
            self.missions[next_index]["name"]
            if next_index < len(self.missions)
            else None
        )
        next_mission = self.get_mission(player.active_mission)
        if next_mission is None:
            print("ALL MISSIONS COMPLETED")
        else:
            print(
                f"MISSION ACTIVE: {next_mission['name']} - "
                f"{next_mission['working_title']}"
            )
        self.start_player_mission(player)
