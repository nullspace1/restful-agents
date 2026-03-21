from typing import Literal

from model.types import Json


type AgentMessageSource = Literal['agent', 'system', 'user']

class Message: 
    def __init__(self, role: AgentMessageSource, content: Json):
        self.role = role
        self.content = content