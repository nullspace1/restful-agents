from src.memory.message_matcher import MessageMatcher
from src.utils.data import DataProvider


class Archive():
    def __init__(self, data_provider: DataProvider, query_matcher : MessageMatcher):
        self.data_provider = data_provider
        self.query_matcher = query_matcher
        
    def add_memory(self, message):
        self.data_provider.add_data(message)
        
    def query(self, query: str):
        all_memories = self.data_provider.get_data()
        matched_memories = [self.query_matcher.matches(m, query) for m in all_memories]
        matched_memories = [m for m in matched_memories if m is not None]
        matched_memories.sort(key=lambda m: m.relevance_score, reverse=True)
        return matched_memories