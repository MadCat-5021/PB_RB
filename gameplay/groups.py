# gameplay/groups.py

from core.events import (
    SWITCH_PRESSED,
    GROUP_COMPLETED
)


class Group:

    def __init__(self, name, targets, event_bus):
        self.name = name
        self.targets = set(targets)
        self.hit_targets = set()
        self.event_bus = event_bus

        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

    def on_switch_pressed(self, event_type, data):

        switch = data["switch"]

        if switch not in self.targets:
            return

        self.hit_targets.add(switch)

        if self.hit_targets == self.targets:

            self.event_bus.publish(
                GROUP_COMPLETED,
                {
                    "group": self.name
                }
            )

            self.hit_targets.clear()