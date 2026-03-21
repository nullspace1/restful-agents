from __future__ import annotations

from typing import TYPE_CHECKING

from model.operation_result import AgentViewable
from model.types import ResourceViewDict
 
if TYPE_CHECKING:
    from typing import Any

    from model.agent import Agent
    from model.resource import Resource
    from model.types import Json, JsonDict


class API(AgentViewable):
    
    def __init__(self, name : str, description : str, resources : list[Resource[Any]]):
        self.name : str = name
        self.description : str = description
        self.resources : set[Resource[Any]] = set(resources)
        self.api_updates : list[Resource[Any]] = []

    def mount(self, resource: Resource[Any]) -> None:
        self.resources.add(resource)
        self.api_updates.append(resource)

    def get(self, agent : Agent, path : str) -> Resource[Any] | None:
        for resource in self.resources:
            view : ResourceViewDict | None  = resource.view(agent)
            if view and view["name"] == path:
                return resource
    
    def search(self, agent : Agent, query : str, depth : int) -> Json:
        matching_resources : list[Json] = []
        for resource in self.resources:
            view : ResourceViewDict | None  = resource.view(agent)
            if view and query in view["name"]:
                if (len(view["name"].split("/")) - len(query.split("/")) <= depth):
                    matching_resources.append(view)
                else:
                    matching_resources.append({"name": view["name"]})
        return matching_resources
    
    def get_updates(self) -> list[Resource[Any]]:
        updates = self.api_updates
        self.api_updates = []
        return updates

    def view(self, agent : Agent) -> JsonDict | None:
        return {
            "name": self.name,
            "description": self.description,
            "root_resources": self.search(agent, "", depth=0) or []
        }
        
    def get_property(self,  agent: Agent, key: str) -> Json | None:
        value = self.view(agent)
        if value:
            return value.get(key)