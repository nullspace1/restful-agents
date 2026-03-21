from __future__ import annotations

import datetime
from typing import TypedDict, TYPE_CHECKING
from .events import Event

if TYPE_CHECKING:
    from ..agent import Agent
    from ..message import Message


class AgentMessageEventData(TypedDict):
    agent: 'Agent'
    message: 'Message'
    timestamp: datetime.datetime


def agent_message_event(agent: "Agent", message: 'Message', timestamp: datetime.datetime | None = None):
    return Event[AgentMessageEventData](
        event_data={
            "agent": agent,
            "message": message,
            "timestamp": timestamp or datetime.datetime.now(),
        },
        to_string=lambda event: f"{event['agent']} said '{event['message']}' at {event['timestamp']}",
    )
