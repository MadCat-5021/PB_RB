from core.event_bus import EventBus
from core.events import (
    SEQUENCE_COMPLETED,
    SEQUENCE_RESET,
    GROUP_COMPLETED
)
from gameplay.groups import Group
from gameplay.sequences import Sequence
from input.input_manager import InputManager

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

    bus = EventBus()

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
    Sequence(
        name="TEST_SEQUENCE",
        targets=["A", "B", "C"],
        event_bus=bus
    )
    Group(
        name="TEST_GROUP",
        targets=["D", "E", "F"],
        event_bus=bus
    )
    input_manager = InputManager(bus)

    print("PB_RB Test Environment")
    print("Enter switches: A, B or C")
    print()

    input_manager.run()


if __name__ == "__main__":
    main()