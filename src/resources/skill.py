from typing import Any, Callable

from model.agent import Agent
from model.auth import KeySet, generate_auth_key
from model.operation import Operation
from model.operation_result import AgentViewableValue, OperationResult, OperationStatus
from model.parameter import ParameterTemplate
from model.resource import Resource
from model.types import Json, ResourceKeyPair


def post(resource : Resource[Callable[[dict[str,str]], Json]], agent : Agent, params : dict[str, Any]) -> OperationResult:
    try:
        return {
            "status": OperationStatus.CONTINUE,
            "output": AgentViewableValue(resource.data(params))
        }
    except Exception as e:
        return {
            "status": OperationStatus.FAIL,
            "output": AgentViewableValue({"error": str(e)})
        }
    
    
def skill(
    owner: Agent,
    name: str,
    description: str,
    param_templates: list[ParameterTemplate],
    func: Callable[[dict[str, str]], Json]
) -> ResourceKeyPair:
    keyset : KeySet = KeySet(post=generate_auth_key())
    return (keyset, Resource[Callable[[dict[str, str]], Json]](
        owner=owner,
        group=None,
        name=name,
        description=description,
        auth_keys=keyset,
        data=func,
        post_op=Operation[Callable[[dict[str, str]], Json]](
            operation=post,
            param_templates=param_templates,
            description="Execute the function with the given parameters"
        )
    ))