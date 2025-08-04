import uuid

class Event:
    def __init__(self, event_type, sub_type=None, data=None):
        self.event_type = event_type
        self.sub_type = sub_type
        self.data = data
        self.uuid = str(uuid.uuid4())

class PubSub:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, sub_type=None, callback=None):
        key = (event_type, sub_type)
        if key not in self.subscribers:
            self.subscribers[key] = []
        self.subscribers[key].append(callback)

    def unsubscribe(self, event_type, sub_type=None, callback=None):
        key = (event_type, sub_type)
        if key in self.subscribers:
            self.subscribers[key] = [
                cb for cb in self.subscribers[key] if cb != callback
            ]

    def publish(self, event_type, sub_type=None, data=None):
        event = Event(event_type, sub_type, data)
        key = (event_type, sub_type)
        for callback in self.subscribers.get(key, []):
            callback(event)



- Change Detection (event emission)
- Effect Analysis (event listening, emission)
- Impact Analysis (event emission)
- Collator (reporter)

event UUID - Change Connector

# Project: Scratch Event Emitter
def event_emitter(event_type, data=None):
    """
    Emit an event with the specified type and data.
    
    Args:
        event_type (str): The type of the event to emit.
        data (any, optional): Additional data to pass with the event.
    """
    pubsub.publish(event_type, data)

def event_listener(event_type, callback):
    """
    Register a callback to listen for events of a specific type.
    
    Args:
        event_type (str): The type of the event to listen for.
        callback (callable): The function to call when the event is emitted.
    """
    pubsub.subscribe(Connector, callback)

# Example usage:
if __name__ == "__main__":
    pubsub = PubSub()

    def on_event(data):
        print(f"Received event with data: {data}")

    pubsub.subscribe("test_event", on_event)
    pubsub.publish("test_event", {"foo": "bar"})