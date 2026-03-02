from src.utils.data import DataProvider
from src.utils.token import TokenCounter
from src.memory.message import Message


class MemoryBuffer:
    
    def __init__(self, data_provider : DataProvider[Message], token_counter : TokenCounter, token_limit : int = 300, min_message_in_buffer : int = 5):
        self.data_provider = data_provider
        self.token_counter = token_counter
        self.token_limit = token_limit
        self.min_message_in_buffer = min_message_in_buffer
        
    def add_memory(self, message: Message) -> None:
        self.data_provider.add_data(message)
        
    def get_recent_memories(self) -> list[Message]:
        memories = self.data_provider.get_data()
        memories.sort(key=lambda m: m.timestamp, reverse=True)
        return memories
    
    def is_within_token_limit(self) -> bool:
        memories = self.get_recent_memories()
        total_tokens = sum(self.token_counter.count_tokens(m.content) for m in memories)
        return total_tokens <= self.token_limit
    
    def clear_memories(self) -> None:
        recent_messages = self.get_recent_memories()[:self.min_message_in_buffer]
        self.data_provider.clear_data()
        for message in recent_messages:
            self.data_provider.add_data(message)
            