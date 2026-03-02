from src.memory.message import Message
from src.memory.summary import Summary
from src.memory.short_term_memory import MemoryBuffer
from src.memory.summarizer_class import Summarizer
from src.memory.archive import Archive


class AgentMemory:
    
    def __init__(self, memory_buffer : MemoryBuffer, summarizer: Summarizer, archive : Archive):
        self.summary = Summary()
        self.memory_buffer = memory_buffer
        self.summarizer = summarizer
        self.memory_archive = archive
        
    def add_memory(self, message: Message) -> None:
        
        self.memory_buffer.add_memory(message)
        self.memory_archive.add_memory(message)
        
        if (not self.memory_buffer.is_within_token_limit()):
            recent_memories = self.memory_buffer.get_recent_memories()
            self.summary = self.summarizer.update_summary(self.summary, recent_memories)
            self.memory_buffer.clear_memories()
            
    def get_memory_buffer(self) -> MemoryBuffer:
        return self.memory_buffer
    
    def get_summary(self) -> Summary:
        return self.summary
    
    def get_memory_archive(self) -> Archive:
        return self.memory_archive
            

            
