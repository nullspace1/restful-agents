from __future__ import annotations

import datetime
from typing import TypedDict, TYPE_CHECKING, Any
from ..enums import OperationType
from .events import Event

if TYPE_CHECKING:
    from ..agent import Agent
    from ..resource import Resource


class ScheduledOperationEventData(TypedDict):
    resource: 'Resource[Any]'
    resource_name: str
    operation_type: OperationType
    parameters: dict[str, Any]
    agent: 'Agent'
    timestamp: datetime.datetime


def scheduled_operation_event(
    resource: "Resource[Any]",
    resource_name: str,
    operation_type: OperationType,
    parameters: dict[str, Any],
    agent: "Agent",
    timestamp: datetime.datetime | None = None,
):
    return Event[ScheduledOperationEventData](
        event_data={
            "resource": resource,
            "resource_name": resource_name,
            "operation_type": operation_type,
            "parameters": parameters,
            "agent": agent,
            "timestamp": timestamp or datetime.datetime.now(),
        },
        to_string=lambda event: f"{event['agent']} scheduled {event['resource']} {event['operation_type']} at {event['timestamp']}",
    )
