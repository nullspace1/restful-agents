from __future__ import annotations

from typing import Generic, TYPE_CHECKING

from model.typebar import D
from model.types import JsonDict

if TYPE_CHECKING:
    from typing import Any, Callable

    from model.resource import Resource
    from model.agent import Agent
    from model.operation_result import OperationResult
    from model.parameter import ParameterTemplate


class Operation(Generic[D]):
    
    def __init__(self, operation : Callable[['Resource[D]','Agent', dict[str, Any]], 'OperationResult'],
                 param_templates : list[ParameterTemplate],
                 description : str = ""):
        self.operation = operation
        self.param_templates = param_templates
        self.description = description
        
    def execute(self, resource : 'Resource[D]', agent : 'Agent', params : dict[str, Any]) -> 'OperationResult':
        for template in self.param_templates:
            if template.required and template.name not in params:
                raise ValueError(f"Required parameter {template.name} is missing.")

            if template.name in params and not template.validate(params[template.name]):
                raise ValueError(f"Parameter {template.name} must be of type {template.type.__name__}.")

        template_names = {template.name for template in self.param_templates}
        for param_name in params:
            if param_name not in template_names:
                raise ValueError(f"Parameter {param_name} is not valid for this operation.")

        return self.operation(resource, agent, params)
    
    def view(self) -> JsonDict:
        return {
            "description": self.description, "parameters": [{
            'name': template.name,
            'description': template.description,
            'required': template.required
           
        } for template in self.param_templates]}
