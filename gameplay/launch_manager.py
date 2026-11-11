# gameplay/launch_manager.py

from core.events import (LAUNCH_SEQUENCE,LAUNCH_COMPLETE)

class LaunchManager:

    def __init__(
        self,
        event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe(LAUNCH_SEQUENCE,self.on_launch_sequence)
        self.event_bus.subscribe(LAUNCH_COMPLETE,self.on_launch_complete)

    def on_launch_sequence(
        self,
        event_type,
        data):
        print("LAUNCH SEQUENCE STARTED")

    def on_launch_complete(
        self,
        event_type,
        data):
        print("BALL LAUNCHED")