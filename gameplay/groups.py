# gameplay/groups.py

from core.events import (
    SWITCH_PRESSED,
    GROUP_COMPLETED
)


class Group:
    def __init__(
        self,
        name,
        targets,
        event_bus,
        target_manager
    ):
        self.name = name
        self.targets = targets
        self.event_bus = event_bus
        self.target_manager = target_manager
        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

    def on_switch_pressed(self, event_type, data):
        if self.is_completed():
            self.event_bus.publish(
                GROUP_COMPLETED,
                {
                    "group": self.name
                }
            )
            self.target_manager.reset_targets(
                self.targets
            )

    def is_completed(self):
        for target_name in self.targets:
            if not self.target_manager.get_hit_state(
                target_name
            ):
                return False
        return True
