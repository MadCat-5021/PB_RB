# gameplay/target_manager.py

from core.events import SWITCH_PRESSED
from content.targets import TARGETS
from time import time

class TargetManager:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.targets = {
            target["name"]: target
            for target in TARGETS
        }
        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

    def on_switch_pressed(self, event_type, data):
        target_name = data["switch"]
        if target_name not in self.targets:
            return
        target = self.targets[target_name]
        target["hit_count"] += 1
        target["hit_last_time"] = time()
        if target["hit_type"] == "LATCHING":
            target["hit_state"] = True
        print(
            f"TARGET HIT: {target_name} "
            f"(count={target['hit_count']})"
        )

    def get_target(self, target_name):
        return self.targets.get(target_name)

    def get_hit_state(self, target_name):
        if target_name not in self.targets:
            return False
        return self.targets[target_name]["hit_state"]

    def get_hit_count(self, target_name):
        if target_name not in self.targets:
            return 0
        return self.targets[target_name]["hit_count"]

    def reset_target(self, target_name):
        if target_name not in self.targets:
            return
        self.targets[target_name]["hit_state"] = False

    def reset_targets(self, target_names):
        for target_name in target_names:
            self.reset_target(target_name)