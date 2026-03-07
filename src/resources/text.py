from __future__ import annotations

from typing import Any

from src.model.resource import Resource, PermissionLevel
from src.model.operation import Operation
from src.model.parameter import ParameterTemplate
from src.model.user import Group, User


def get(resource : Resource[str], user : User, params : dict[str, Any] | None = None) -> dict[str, str]:
    return {
    "content": resource.data or ""}

def patch(resource : Resource[str], user : User, params : dict[str, Any]) -> dict[str, str]:
    if not resource.data:
        resource.data = ""
    resource.data = params.get("content", "")
    return {"content": resource.data or ""}

def delete(resource : Resource[str], user : User, params : dict[str, Any]) -> dict[str, str]:
    resource.data = ""
    return {"status": "content deleted"}


def text(
    user : User,
    group : Group, 
    user_permissions : PermissionLevel, 
    group_permissions : PermissionLevel, 
    other_permissions : PermissionLevel,
    text_summary : str,
    text : str
    ) -> Resource[str]:
    return Resource[str](
        owner=user,
        group=group,
        type="text",
        name="text",
        description=text_summary,
        user_permissions=user_permissions,
        group_permissions=group_permissions,
        other_permissions=other_permissions,
        data=text,
        get_op=Operation[str](
            operation=get,
            param_templates=[],
            description="Retrieve the text content"
        ),
        patch_op=Operation[str](
            operation=patch,
            param_templates=[
                ParameterTemplate("content", "The text content to store", str, required=True)],
            description="Update the text content"
        ),
        delete_op=Operation[str](
            operation=delete,
            param_templates=[],
            description="Delete the text content"
        )
    )