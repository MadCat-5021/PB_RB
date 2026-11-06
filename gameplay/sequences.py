# gameplay/sequences.py

from core.events import (
    SWITCH_PRESSED,
    SEQUENCE_COMPLETED,
    SEQUENCE_RESET
)


class Sequence:
    def __init__(
        self,
        name,
        targets,
        event_bus
    ):
        self.name = name
        self.targets = targets
        self.event_bus = event_bus
        self.current_index = 0
        self.event_bus.subscribe(
            SWITCH_PRESSED,
            self.on_switch_pressed
        )

    def on_switch_pressed(
        self,
        event_type,
        data
    ):
        switch = data["switch"]
        print(
            f"SEQUENCE {self.name}: "
            f"received {switch}"
        )
        # Sequence nog niet gestart
        if self.current_index == 0:
            if switch == self.targets[0]:
                self.current_index = 1
                # Sequence van slechts 1 target
                if len(self.targets) == 1:
                    self.event_bus.publish(
                        SEQUENCE_COMPLETED,
                        {
                            "sequence": self.name
                        }
                    )
                    self.current_index = 0
            return

        expected_switch = self.targets[self.current_index]
        # Correcte volgende stap
        if switch == expected_switch:
            self.current_index += 1
            # Sequence voltooid
            if self.current_index == len(self.targets):
                self.event_bus.publish(
                    SEQUENCE_COMPLETED,
                    {
                        "sequence": self.name
                    }
                )
                self.current_index = 0
            return
        # Verkeerde target nadat sequence gestart is
        print(
            f"SEQUENCE {self.name}: RESET"
        )
        self.current_index = 0
        self.event_bus.publish(
            SEQUENCE_RESET,
            {
                "sequence": self.name
            }
        )