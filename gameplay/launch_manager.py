# gameplay/launch_manager.py

class LaunchManager:

    def __init__(
        self,
        event_bus):

        self.event_bus = event_bus

        self.event_bus.subscribe(
            LAUNCH_SEQUENCE,
            self.on_launch_sequence)

    def on_launch_sequence(
        self,
        event_type,
        data):

        print(
            "LAUNCH SEQUENCE STARTED")