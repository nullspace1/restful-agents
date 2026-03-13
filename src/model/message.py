from __future__ import annotations

import datetime


class Message:
    
    def __init__(self,user : str, content: str, timestamp: datetime.datetime | None = None):
        self.user = user
        self.content = content
        self.timestamp = timestamp or datetime.datetime.now()
        
    def __str__(self) -> str:
        return f"[{self.timestamp.isoformat()}] [{self.user}]: {self.content}"
