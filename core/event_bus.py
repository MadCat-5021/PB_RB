# core/event_bus.py

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        """
        Register a callback for an event type.
        """

        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        """
        Remove a callback from an event type.
        """

        if event_type not in self._subscribers:
            return

        try:
            self._subscribers[event_type].remove(callback)
        except ValueError:
            pass

    def publish(self, event_type, data=None):
        """
        Publish an event to all subscribers.
        """

        if event_type not in self._subscribers:
            return

        for callback in self._subscribers[event_type]:
            callback(event_type, data)
