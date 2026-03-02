import datetime
from abc import ABC, abstractmethod

from src.memory.message import Message
from src.memory.summarizer_class import Summarizer
from src.user.user import User

class SummaryItem(ABC):
    """Base class for all summary items"""
    
    def __init__(self, source : User, details: str, evidence: list[Message]):
        self.source = source
        self.details = details
        self.evidence = evidence
    
    @abstractmethod
    def display(self) -> str:
        """Display the summary item as a formatted string"""
        pass
    
    def display_date(self, date: datetime.datetime) -> str:
        secondsSince : int = (datetime.datetime.now() - date).total_seconds()
        hoursSince : int = int(secondsSince / 3600)
        daysSince : int = int(secondsSince / 86400)
        minutesSince : int = int(secondsSince / 60)
        if daysSince == 0:
            if hoursSince == 0:
                return "just now" if minutesSince == 0 else f"{minutesSince} minutes ago"
            else:
                return f"{hoursSince} hours ago"
        elif daysSince == 1:
            return "yesterday"
        else:
            return f"{daysSince} days ago"

class Booking(SummaryItem):
    
    def __init__(self, booking_id: str, source: User, start_date: datetime.datetime, end_date: datetime.datetime,  details: str, amount_paid: float, evidence : list[Message]):
        super().__init__(source, details, evidence)
        self.booking_id = booking_id
        self.start_date = start_date
        self.end_date = end_date
        self.amount_paid = amount_paid
    
    def display(self) -> str:
        return f"Booking {self.booking_id}: {self.display_date(self.start_date)} to {self.display_date(self.end_date)} - {self.details} (${self.amount_paid})"
        
class Request(SummaryItem): 
    
    def __init__(self, request_id: str, source: User, date: datetime.datetime, details: str, evidence: list[Message]):
        super().__init__(source, details, evidence)
        self.request_id = request_id
        self.date = date
    
    def display(self) -> str:
        return f"Request {self.request_id}: {self.display_date(self.date)} - {self.details}"
        
class Reservation(SummaryItem):
    
    def __init__(self, reservation_id: str, source: User, start_date: datetime.datetime, end_date: datetime.datetime, initial_payment: float, details: str, evidence: list[Message]):
        super().__init__(source, details, evidence)
        self.reservation_id = reservation_id
        self.start_date = start_date
        self.end_date = end_date
        self.initial_payment = initial_payment
    
    def display(self) -> str:
        return f"Reservation {self.reservation_id}: {self.display_date(self.start_date)} to {self.display_date(self.end_date)} - {self.details} (${self.initial_payment})"
        
        
class Fact(SummaryItem): 
    
    def __init__(self, fact_id: str, source: User, date: datetime.datetime, details: str, evidence: list[Message]):
        super().__init__(source, details, evidence)
        self.fact_id = fact_id
        self.date = date
    
    def display(self) -> str:
        return f"Fact {self.fact_id}: {self.display_date(self.date)} - {self.details}"
        
class Task(SummaryItem):
    
    def __init__(self, task_id: str, source: User, date: datetime.datetime, details: str, evidence: list[Message]):
        super().__init__(source, details, evidence)
        self.task_id = task_id
        self.date = date
    
    def display(self) -> str:
        return f"Task {self.task_id}: {self.display_date(self.date)} - {self.details}"

class Summary:
    
    def __init__(self):
        self.items : SummaryItem = []
        
    def add_item(self, item: SummaryItem) -> None:
        self.items.append(item)
        
    def display(self) -> str:
        return "\n".join(item.display() for item in self.items)
