from abc import ABC, abstractmethod
from typing import List, Optional
from src.todo_list.infrastructure.database.models.project import ProjectModel

class IProjectRepository(ABC):
    @abstractmethod
    def create(self, project: ProjectModel) -> ProjectModel:
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[ProjectModel]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[ProjectModel]:
        pass
    
    @abstractmethod
    def update(self, project: ProjectModel) -> ProjectModel:
        pass
    
    @abstractmethod
    def delete(self, project_id: int) -> bool:
        pass