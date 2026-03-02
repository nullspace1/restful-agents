from abc import ABC, abstractmethod
from src.memory.message import Message
from src.memory.summary import Summary


class Summarizer(ABC):
    
    @abstractmethod
    def update_summary(self, current_summary: Summary, memories: list[Message]) -> Summary:
        pass
