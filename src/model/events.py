from __future__ import annotations

from abc import ABC, abstractmethod
import datetime
from typing import Any, Generic
from src.model.enums import  OperationType, Status
from src.model.operation import Operation
from src.model.resource import Resource
from src.model.user import User
from src.model.types import D

class Event(Generic[D]):
    
    def __init__(self, resource : Resource[D], operation : Operation[D], operation_type : OperationType, status : Status, output : Any, parameters : dict[str, Any], user : 'User', exception : Exception | None = None, timestamp : datetime.datetime | None = None):
        self.resource = resource
        self.operation = operation
        self.operation_type = operation_type
        self.status = status
        self.parameters = parameters
        self.user = user
        self.output = output
        self.timestamp = timestamp or datetime.datetime.now()
        self.exception = exception
    def __str__(self) -> str:
        return f"{self.timestamp.isoformat()} - {self.user.name} performed {self.operation_type.name} on {self.resource.name} with status {self.status.name}. Parameters: {self.parameters}. Output: {self.output}"


class EventListener(ABC, Generic[D]):
    
    @abstractmethod
    def notify(self, event : Event[D]):
        pass

class EventEmitter(Generic[D]):
    
    def __init__(self):
        self.listeners : dict[tuple[Resource[D], list[OperationType]], list[EventListener[D]]] = {}
        
    def emit(self, event : Event[D]):
        for (resource, operations), listeners in self.listeners.items():
            if resource == event.resource and event.operation_type in operations:
                for listener in listeners:
                    listener.notify(event)
        if self != GLOBAL_EMITTER:
            GLOBAL_EMITTER.emit(event)
            
    def add_listener(self, listener : EventListener[D], resource : Resource[D], operations : list[OperationType] | None = None):
        if operations is None:
            operations = [OperationType.GET, OperationType.POST, OperationType.PATCH, OperationType.DELETE]
        self.listeners.setdefault((resource, operations), []).append(listener)
        
        
GLOBAL_EMITTER = EventEmitter[Any]()
    