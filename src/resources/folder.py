from __future__ import annotations

from typing import Any, cast

from src.model.resource import PermissionLevel, Resource
from src.model.user import Group, User
from src.model.operation import Operation
from src.model.parameter import ParameterTemplate


def sanitize_path(path: str) -> list[str]:
    parts = path.split("/")
    parts = [p.strip() for p in parts if p.strip()]
    return parts

def get(resource : Resource[list[Resource[Any]]], user : User, params : dict[str, Any]) -> dict[str, str]:
    path_str = params.get("path", "")
    path = sanitize_path(path_str) if path_str else []
    
    if not path:
        if resource.data:
            contents = ", ".join([r.name for r in resource.data])
            return {"contents": contents}
        return {"contents": "empty"}
    
    target_name = path[0]
    
    target_resource = None
    if resource.data:
        for r in resource.data:
            if r.name == target_name:
                target_resource = r
                break
    
    if not target_resource:
        raise ValueError(f"Resource '{target_name}' not found in folder '{resource.name}'")
    
    if len(path) > 1:
        if target_resource.type != "folder":
            raise ValueError(f"Resource '{target_name}' is not a folder, cannot navigate further")
        remaining_path = "/".join(path[1:])
        return target_resource.get(user, {"path": remaining_path})
    else:
        return target_resource.get(user, {})
    
def delete(resource : Resource[list[Resource[Any]]], user : User, params : dict[str, Any]) -> dict[str, str]:
    path_str = params.get("path", "")
    path = sanitize_path(path_str) if path_str else []
    
    if not path:
        resource.data = []
        return {"status": "folder cleared"}
    
    target_name = path[0]
    
    target_resource = None
    if resource.data:
        for r in resource.data:
            if r.name == target_name:
                target_resource = r
                break
    
    if not target_resource:
        raise ValueError(f"Resource '{target_name}' not found in folder '{resource.name}'")
    
    if len(path) > 1:
        if target_resource.type != "folder":
            raise ValueError(f"Resource '{target_name}' is not a folder, cannot navigate further")
        remaining_path = "/".join(path[1:])
        return target_resource.delete(user, {"path": remaining_path})
    else:
        resource.data.remove(target_resource)
        return {"status": f"Resource '{target_name}' deleted from folder '{resource.name}'"}

def post(resource : Resource[list[Resource[Any]]], user : User, params : dict[str, Any]) -> dict[str, str]:
    
    new_resource : Resource[Any] = cast(Resource[Any], params.get("resource"))
    path_str = params.get("path", "")
    path = sanitize_path(path_str) if path_str else []
    
    if not path:
        if not resource.data:
            resource.data = []
        resource.data.append(new_resource)
        return {"status": f"Resource '{new_resource.name}' added to folder '{resource.name}'"}
    
    target_name = path[0]
    
    target_resource = None
    
    for r in resource.data:
        if r.name == target_name:
            target_resource = r
            break
    
    if not target_resource:
        raise ValueError(f"Resource '{target_name}' not found in folder '{resource.name}'")
    
    if len(path) > 1:
        if target_resource.type != "folder":
            raise ValueError(f"Resource '{target_name}' is not a folder, cannot navigate further")
        remaining_path = "/".join(path[1:])
        return target_resource.post(user, {"path": remaining_path, "resource": new_resource})
    
    if not new_resource:
        raise ValueError("No resource provided to add to folder")
    
    resource.data.append(new_resource)
    return {"status": f"Resource '{new_resource.name}' added to folder '{resource.name}'"}

def folder(
    user : User,
    group : Group, 
    folder_name : str,
    user_permissions : PermissionLevel, 
    group_permissions : PermissionLevel, 
    other_permissions : PermissionLevel,
    ) -> Resource[list[Resource[Any]]]: 
    return Resource(
        owner=user,
        group=group,
        type="folder",
        name=folder_name,
        description=f"A folder resource named {folder_name} that can contain other resources",
        user_permissions=user_permissions,
        group_permissions=group_permissions,
        other_permissions=other_permissions,
        data=[],
        get_op=Operation[list[Resource[Any]]](
            operation=get,
            param_templates=[ParameterTemplate("path", "Path to navigate within the folder", str, required=False)],
            description="Get a resource from the folder by path"
        ),
        delete_op=Operation[list[Resource[Any]]](
            operation=delete,
            param_templates=[ParameterTemplate("path", "Path to navigate within the folder", str, required=False)],
            description="Delete a resource from the folder by path"
        ),
        post_op=Operation[list[Resource[Any]]](
            operation=post,
            param_templates=[
                ParameterTemplate("path", "Path to navigate within the folder", str, required=False),
                ParameterTemplate("resource", "The resource to add to the folder", Resource, required=True)
            ],
            description="Add a resource to the folder at the specified path"
        )
    )