from __future__ import annotations

from typing import Callable, Generic, Any
from model.typebar import D


class Event(Generic[D]):

    def __init__(self, event_data: D, to_string: Callable[[D], str]):
        self.event_data = event_data
        self.to_string = to_string

    def __str__(self) -> str:
        return self.to_string(self.event_data)


class EventListener(Generic[D]):

    def __init__(self, callback: Callable[[Event[D]], None]):
        self.callback = callback

    def notify(self, event: Event[D]):
        self.callback(event)


class EventEmitter(Generic[D]):

    def __init__(self):
        self.listeners: list[EventListener[D]] = []

    def emit(self, event: Event[D]):
        for listener in self.listeners:
            listener.notify(event)
        if self != GLOBAL_EMITTER:
            GLOBAL_EMITTER.emit(event)

    def add_listener(self, listener: EventListener[D]):
        self.listeners.append(listener)


GLOBAL_EMITTER = EventEmitter[Any]()
