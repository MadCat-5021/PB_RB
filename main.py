from core.event_bus import EventBus
from core.events import (
    SWITCH_PRESSED,
    SEQUENCE_COMPLETED,
    SEQUENCE_RESET
)

from gameplay.sequences import Sequence


bus = EventBus()

sequence = Sequence(
    name="TEST_SEQUENCE",
    targets=["A", "B", "C"],
    event_bus=bus
)


def on_sequence_completed(event_type, data):
    print("SEQUENCE COMPLETED")
    print(data)


def on_sequence_reset(event_type, data):
    print("SEQUENCE RESET")
    print(data)


bus.subscribe(
    SEQUENCE_COMPLETED,
    on_sequence_completed
)

bus.subscribe(
    SEQUENCE_RESET,
    on_sequence_reset
)


print("Testing A -> B -> C")

bus.publish(
    SWITCH_PRESSED,
    {"switch": "A"}
)

bus.publish(
    SWITCH_PRESSED,
    {"switch": "B"}
)

bus.publish(
    SWITCH_PRESSED,
    {"switch": "C"}
)