from typing import Any

from model.agent import Agent
from model.operation_result import AgentViewable, JsonLike
from model.resource import Resource

class APINode:
    
    def __init__(self, name : str, children : list['APINode'], is_resource : bool):
        self.name = name
        self.children = children
        self.is_resource = is_resource

class API(AgentViewable):
    
    def __init__(self, name : str, description : str, resources : list[Resource[Any]]):
        self.name : str = name
        self.description : str = description
        self.resources : set[Resource[Any]] = set(resources)
        self.__path_graph__ : APINode = APINode('', [], False)
        self.__graph_dirty__ : bool = bool(resources)

    def mount(self, agent: Agent, resource: Resource[Any]):
        self.resources.add(resource)
        self.__graph_dirty__ = True

    def get(self, agent : Agent, path : str) -> Resource[Any] | None:
        self.__ensure_graph__(agent)
        for resource in self.resources:
            view : JsonLike | None = resource.view(agent)
            if view and view['name'] == path:
                return resource
    def search(self, agent : Agent, query : str, depth : int = 0, root_node : APINode | None = None) -> JsonLike | None:
        self.__ensure_graph__(agent)
        
        root : APINode = root_node if root_node else self.__path_graph__
         
        node : APINode | None = self.__find_node__(root, query)
        
        if not node:
            return None
        
        if node.is_resource:
            res = self.get(agent, query)
            return res.view(agent) if res else None
        else:
            visible_children = [c for c in node.children if self.__has_visible_resource__(agent, c)]
            
            if depth == 0:
                data : JsonLike = {
                    "name": node.name,
                    "description": f"This path contains {len(visible_children)} sub-resources"
                }     
            else:
                search_result = [self.search(agent, f"{node.name}/{c.name}", depth - 1, c) for c in visible_children]
                data : JsonLike = [r for r in search_result if r is not None]
                
            return data
        
    def __has_visible_resource__(self, agent: Agent, node: APINode) -> bool:
        count = 0
        for r in self.resources:
            view = r.view(agent)
            if view is not None:
                name : str = view.get('name')
                if name.startswith(node.name):
                        count += 1
        return count > 0
        
    def __ensure_graph__(self, agent: Agent) -> None:
        if self.__graph_dirty__:
            self.__rebuild_path_graph__(agent)

    def __rebuild_path_graph__(self, agent: Agent) -> None:
        root = APINode('', [], False)
        for resource in self.resources:
            view = resource.view(agent)
            if view is None:
                continue
            name : str = view['name']
            split_path : list[str] = name.split('/')
            current_node = root
            for part in split_path:
                found_node = None
                for child in current_node.children:
                    if child.name == part:
                        found_node = child
                        break
                if not found_node:
                    found_node = APINode(part, [], False)
                    current_node.children.append(found_node)
                current_node = found_node
            current_node.is_resource = True
        self.__path_graph__ = root
        self.__graph_dirty__ = False
        
    def __find_node__(self,root_node : APINode, query : str) -> APINode | None:
        split_query : list[str] = query.split('/')
        current_node = root_node
        
        for part in split_query:
            found_node = None
            for child in current_node.children:
                if child.name == part:
                    found_node = child
                    break
            if not found_node:
                return None
            current_node = found_node
        return current_node
        
        
    def view(self, agent : Agent) -> JsonLike:
        return {
            "name": self.name,
            "description": self.description,
            "root_resources": self.search(agent, "", depth=0) or []
        }

class Browser:
    
    def __init__(self):
        self.api : dict[str, API] = {}
        
    def mount_api(self, name: str, api: API):
        self.api[name] = api
