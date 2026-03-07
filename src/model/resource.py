from __future__ import annotations

import datetime
from typing import Any, Generic

from src.model.enums import OperationType, Status
from src.model.user import User, Group
from src.model.operation import Operation
from src.model.events import Event, EventEmitter
from src.model.types import D

class PermissionLevel:
    
    def __init__(self, 
                 get : bool, 
                 post : bool, 
                 patch : bool, 
                 delete : bool):
        self.permissions = {
            OperationType.GET: get,
            OperationType.POST: post,
            OperationType.PATCH: patch,
            OperationType.DELETE: delete}
    
    def verify(self, operation : OperationType) -> bool:
        return self.permissions[operation]
    
    def get_permissions(self) -> dict[str, bool]:
        return {
            "get": self.permissions[OperationType.GET],
            "post": self.permissions[OperationType.POST],
            "patch": self.permissions[OperationType.PATCH],
            "delete": self.permissions[OperationType.DELETE]
        }
    

class Resource(Generic[D], EventEmitter[D]):
    
    def __init__(self, 
                 owner : User, 
                 group : Group, 
                 type : str,
                 name : str,
                 description : str,
                 user_permissions : PermissionLevel, 
                 group_permissions : PermissionLevel, 
                 other_permissions : PermissionLevel,
                 data : D,
                 get_op : Operation[D] | None = None, 
                 post_op : Operation[D] | None = None,
                 patch_op : Operation[D] | None = None,
                 delete_op : Operation[D] | None = None,
                 created_at : datetime.datetime | None = None, 
                 ):
        super().__init__()
        self.name : str = name
        self.description : str = description
        self.type : str  = type
        self.created_at : datetime.datetime = created_at or datetime.datetime.now()
        self.owner : User = owner
        self.group : Group = group
        self.get_op : Operation[D] | None = get_op
        self.post_op : Operation[D] | None = post_op
        self.patch_op : Operation[D] | None = patch_op
        self.delete_op : Operation[D] | None = delete_op
        self.user_permissions : PermissionLevel = user_permissions
        self.group_permissions : PermissionLevel = group_permissions
        self.other_permissions : PermissionLevel = other_permissions
        self.data : D  = data
        
    def get(self, user : User, params : dict[str, Any] | None = None) -> dict[str, str]:
        """Retrieve the full resource contents.
        
        Fetches the complete contents of the resource (e.g., file contents, collection tree).
        Requires GET permission. Emits a SUCCESS or FAILURE event upon completion.
        
        Args:
            user: The user performing the operation. Must have GET permission.
            params: Optional dictionary of parameters to pass to the operation handler.
        
        Returns:
            Any: The full resource contents, which can be of any type depending on the resource (e.g., string for file contents, list of child resources for a collection).
        
        Raises:
            PermissionError: If the user does not have GET permission on this resource.
            Exception: Any exception raised by the operation handler is re-raised after emitting a FAILURE event.
        """
        if not self.get_op:
            raise NotImplementedError("GET operation is not implemented for this resource.")
        if not self.__verify_permissions(user, OperationType.GET):
            raise PermissionError("You do not have permission to GET this file.")
        try: 
            result = self.get_op.execute(self,user, params or {})
            self.emit(Event(self, self.get_op, OperationType.GET, Status.SUCCESS, result, params or {}, user))
            return result
        except Exception as e:
            self.emit(Event(self, self.get_op, OperationType.GET, Status.FAILURE, None, params or {}, user, e))
            raise
            
    def post(self, user : User, params : dict[str, Any]) -> dict[str, str]:
        """Add new content to the resource.
        
        Appends or adds new content to the resource (e.g., appending to a file or adding 
        a new resource to a collection). Requires POST permission. Emits a SUCCESS or FAILURE event upon completion.
        
        Args:
            user: The user performing the operation. Must have POST permission.
            params: Dictionary of parameters to pass to the operation handler (required).
        
        Returns:
            Describable: Result of the post operation, which can be of any type depending on the operation handler.
        
        Raises:
            PermissionError: If the user does not have POST permission on this resource.
            Exception: Any exception raised by the operation handler is re-raised after emitting a FAILURE event.
        """
        if not self.post_op:
            raise NotImplementedError("POST operation is not implemented for this resource.")
        if not self.__verify_permissions(user, OperationType.POST):
            raise PermissionError("You do not have permission to POST to this file.")
        try:
            result = self.post_op.execute(self, user, params)
            self.emit(Event(self, self.post_op, OperationType.POST, Status.SUCCESS, result, params, user))
            return result
        except Exception as e:
            self.emit(Event(self, self.post_op, OperationType.POST, Status.FAILURE, None, params, user, e))
            raise
            
    def patch(self, user : User, params : dict[str, Any]) -> dict[str, str]:
        """Modify existing content in the resource.
        
        Updates or modifies existing content in the resource (e.g., updating file contents 
        or modifying a resource in a collection). Requires PATCH permission. Emits a SUCCESS or FAILURE event upon completion.
        
        Args:
            user: The user performing the operation. Must have PATCH permission.
            params: Dictionary of parameters to pass to the operation handler (required).
        
        Returns:
            Resource[D]: Result of the patch operation.
        
        Raises:
            PermissionError: If the user does not have PATCH permission on this resource.
            Exception: Any exception raised by the operation handler is re-raised after emitting a FAILURE event.
        """
        if not self.patch_op:
            raise NotImplementedError("PATCH operation is not implemented for this resource.")
        if not self.__verify_permissions(user, OperationType.PATCH):
            raise PermissionError("You do not have permission to PATCH this file.")
        try:
            result = self.patch_op.execute(self,     user, params)
            self.emit(Event(self, self.patch_op, OperationType.PATCH, Status.SUCCESS, result, params, user))
            return result
        except Exception as e:
            self.emit(Event(self, self.patch_op, OperationType.PATCH, Status.FAILURE, None, params, user, e))
            raise
            
    def delete(self, user : User, params : dict[str, Any] | None = None) -> dict[str, str]:
        """Remove content from the resource.
        
        Deletes or removes content from the resource (e.g., deleting a file or removing 
        a resource from a collection). Requires DELETE permission. Emits a SUCCESS or FAILURE event upon completion.
        
        Args:
            user: The user performing the operation. Must have DELETE permission.
            params: Optional dictionary of parameters to pass to the operation handler.
        
        Returns:
            Resource[Any]: Result of the delete operation, which can be of any type depending on the operation handler.
        
        Raises:
            PermissionError: If the user does not have DELETE permission on this resource.
            Exception: Any exception raised by the operation handler is re-raised after emitting a FAILURE event.
        """
        if not self.delete_op:
            raise NotImplementedError("DELETE operation is not implemented for this resource.")
        if not self.__verify_permissions(user, OperationType.DELETE):
            raise PermissionError("You do not have permission to DELETE this file.")
        try:
            result = self.delete_op.execute(self, user, params or {})
            self.emit(Event(self, self.delete_op, OperationType.DELETE, Status.SUCCESS, result, params or {}, user))
            return result
        except Exception as e:
            self.emit(Event(self, self.delete_op, OperationType.DELETE, Status.FAILURE, None, params or {}, user, e))
            raise
        
    def view(self, user : User) -> dict[str, Any]:
        """View basic metadata about the resource.
        
        Provides a dictionary representation of the resource's metadata (e.g., name, type, description).
        Requires VIEW permission. Emits a SUCCESS or FAILURE event upon completion.
        
        Args:
            user: The user performing the operation. Must have VIEW permission.
        
        Returns:
            dict[str, Any]: A dictionary representation of the resource's metadata.
            
        Raises:
            PermissionError: If the user does not have VIEW permission on this resource.
        """
        if not self.__verify_permissions(user, OperationType.GET):
            raise PermissionError("You do not have permission to view this resource.")
        return {
                "name": self.name,
                "type": self.type,
                "author": self.owner.name if self.owner else "Unknown",
                "created_at": self.created_at.isoformat(),
                "description": self.description,
                "operations": self.__options(),
                "permissions": {
                    "user": self.user_permissions.get_permissions(),
                    "group": self.group_permissions.get_permissions(),
                    "other": self.other_permissions.get_permissions()
                    }
                }
    
    def __options(self) -> dict[str, str]:
        """
        Provides a dictionary of available operations and their descriptions for this resource.
        """
        ops : dict[str, str] = {}
        if self.get_op:
            ops["get"] = self.get_op.description
        if self.post_op:
            ops["post"] = self.post_op.description
        if self.patch_op:
            ops["patch"] = self.patch_op.description
        if self.delete_op:
            ops["delete"] = self.delete_op.description
        return ops
    
    def __verify_permissions(self, user : User, operation : OperationType) -> bool:
        if user == self.owner:
            return self.user_permissions.verify(operation)
        elif self.group in user.groups:
            return self.group_permissions.verify(operation)
        else:
            return self.other_permissions.verify(operation)
        