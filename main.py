from core.event_bus import EventBus
from core.events import SWITCH_PRESSED


def on_switch_pressed(event_type, data):
    print(f"Event: {event_type}")
    print(f"Data: {data}")


bus = EventBus()

bus.subscribe(
    SWITCH_PRESSED,
    on_switch_pressed
)

bus.publish(
    SWITCH_PRESSED,
    {
        "switch": "LEFT_ORBIT_ENTRY"
    }
)
