from __future__ import annotations


class User:
    
    def __init__(self, uuid : str, name : str, groups : list['Group'] | None = None):
        self.uuid = uuid
        self.name = name
        self.groups = groups or []
        
    def add_group(self, group : 'Group'):
        if group not in self.groups:
            self.groups.append(group)
        
    def remove_group(self, group : 'Group'):
        if group in self.groups:
            self.groups.remove(group)


class Group:
    
    def __init__(self, uuid : str, name : str):
        self.uuid = uuid
        self.name = name
        
ADMIN = Group(uuid="admin", name="Admin")