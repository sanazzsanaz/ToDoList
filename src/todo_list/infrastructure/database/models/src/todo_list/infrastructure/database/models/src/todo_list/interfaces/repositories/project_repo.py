# src/todo_list/interfaces/repositories/project_repo.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ...core.models.project import Project

class IProjectRepository(ABC):
    @abstractmethod
    def create(self, project: Project) -> Project:
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Project]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Project]:
        pass
    
    @abstractmethod
    def update(self, project: Project) -> Project:
        pass
    
    @abstractmethod
    def delete(self, project_id: int) -> bool:
        pass