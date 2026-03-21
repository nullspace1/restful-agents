"""Events package shim.

This exposes the previous `model.events` API while splitting implementation
into smaller modules to avoid circular import issues.
"""
from .events import Event, EventListener, EventEmitter, GLOBAL_EMITTER
from .executed_operation import executed_operation_event, ExecutedOperationEventData
from .agent_message import agent_message_event, AgentMessageEventData
from .scheduled_operation import scheduled_operation_event, ScheduledOperationEventData

__all__ = [
    "Event",
    "EventListener",
    "EventEmitter",
    "GLOBAL_EMITTER",
    "executed_operation_event",
    "ExecutedOperationEventData",
    "agent_message_event",
    "AgentMessageEventData",
    "scheduled_operation_event",
    "ScheduledOperationEventData",
]
