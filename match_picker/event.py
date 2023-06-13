from collections import defaultdict
from typing import Callable

subscribers = defaultdict(list)

def subscribe(event_type: str, fn: Callable):
    """Listen to an event."""
    subscribers[event_type].append(fn)

def post_event(event_type: str, data):
    """Trigger action as event occurs."""
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)
