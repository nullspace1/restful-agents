from dataclasses import dataclass


@dataclass
class User:
    
    id: str
    name: str
    phone_number: str
    
    def __init__(self, id: str, name: str, phone_number: str):
        self.id = id
        self.name = name
        self.phone_number = phone_number
