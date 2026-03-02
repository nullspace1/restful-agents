from abc import ABC, abstractmethod
from typing import Iterator, TypeVar, Generic

T = TypeVar('T')

class DataProvider(ABC, Generic[T]):
    
    @abstractmethod
    def get_data(self) -> list[T]:
        pass

    @abstractmethod
    def add_data(self, data: T):
        pass
    
    @abstractmethod
    def clear_data(self):
        pass