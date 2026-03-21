from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from typing import Any

class ParameterTemplate:    
    def __init__(self, name : str, description : str, converter : Callable[[str], Any], required : bool = True, ):
        self.name = name
        self.description = description
        self.type = type
        self.required = required
        self.converter = converter
        
    def validate(self, value : str) -> bool:
        value = self.converter(value)
        return isinstance(value, self.type)
