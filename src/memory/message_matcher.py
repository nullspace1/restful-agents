from abc import ABC, abstractmethod
from src.memory.message import Message

class RelevantMessage:
    
    def __init__(self, message: Message, relevance_score: float):
        self.message = message
        self.relevance_score = relevance_score

class MessageMatcher(ABC):
    
    @abstractmethod
    def matches(self, message: Message, query: str) -> RelevantMessage:
        pass
