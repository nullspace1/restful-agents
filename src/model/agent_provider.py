from __future__ import annotations

from abc import ABC, abstractmethod

from model.agent import Message


class AgentProvider(ABC):
    @abstractmethod
    def send_message(self, messages: list[Message]) -> str:
        pass

    @abstractmethod
    def count_tokens(self, messages: list[Message]) -> int:
        pass
