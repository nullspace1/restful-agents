from __future__ import annotations

from typing import Callable, Generic

from src.model.parameter import ParameterTemplate
from src.model.resource import Resource
from src.model.user import User
from src.model.types import D
class Operation(Generic[D]):
    
    def __init__(self, operation : Callable[['Resource[D]','User', dict[str, str]], dict[str,str]],
                 param_templates : list[ParameterTemplate],
                 description : str = ""):
        self.operation = operation
        self.param_templates = param_templates
        self.description = description
        
    def execute(self, resource : 'Resource[D]', user : 'User', params : dict[str, str]) -> dict[str, str]:
        for template in self.param_templates:
            if template.required and template.name not in params:
                raise ValueError(f"Required parameter {template.name} is missing.")

            if template.name in params and not template.validate(params[template.name]):
                raise ValueError(f"Parameter {template.name} must be of type {template.type.__name__}.")

        template_names = {template.name for template in self.param_templates}
        for param_name in params:
            if param_name not in template_names:
                raise ValueError(f"Parameter {param_name} is not valid for this operation.")

        return self.operation(resource, user, params)
