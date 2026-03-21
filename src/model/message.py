from typing import Literal


type AgentMessageSource = Literal['agent', 'system', 'user']

class Message: 
    def __init__(self, role: AgentMessageSource, content: str):
        self.role = role
        self.content = content