from core.event_bus import EventBus
from core.events import (
    SEQUENCE_COMPLETED,
    SEQUENCE_RESET,
    GROUP_COMPLETED
)
from gameplay.target_manager import TargetManager
from gameplay.sequences import Sequence
from gameplay.groups import Group
from content.groups import GROUPS
from content.sequences import SEQUENCES
from input.input_manager import InputManager
from content.validator import validate

def on_sequence_completed(event_type, data):
    print()
    print("SEQUENCE COMPLETED")
    print(data)
    print()

def on_group_completed(event_type, data):
    print("GROUP COMPLETED")
    print(data)

def on_sequence_reset(event_type, data):
    print()
    print("SEQUENCE RESET")
    print(data)
    print()

def main():
    validate()
    bus = EventBus()
    target_manager = TargetManager(bus)

    bus.subscribe(
        SEQUENCE_COMPLETED,
        on_sequence_completed
    )

    bus.subscribe(
        SEQUENCE_RESET,
        on_sequence_reset
    )

    bus.subscribe(
        GROUP_COMPLETED,
        on_group_completed
    )

    for sequence in SEQUENCES:
        Sequence(
            name=sequence["name"],
            targets=sequence["targets"],
            event_bus=bus
        )

    for group in GROUPS:
        Group(
            name=group["name"],
            targets=group["targets"],
            event_bus=bus,
            target_manager=target_manager
        )

    input_manager = InputManager(bus)

    print("PB_RB Test Environment")
    print("Enter switches")
    print()

    input_manager.run()

if __name__ == "__main__":
    main()
