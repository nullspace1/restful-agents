from abc import ABC, abstractmethod


class TokenCounter(ABC):
    
    @abstractmethod 
    def count_tokens(self, text: str) -> int:
        pass