import datetime

class Source:
    
    def __init__(self, phone: str, role_at_time: str):
        self.phone = phone
        self.role_at_time = role_at_time


class Message:
    
    def __init__(self, source : Source, content: str, timestamp: datetime.datetime):
        self.source = source
        self.content = content
        self.timestamp = timestamp
