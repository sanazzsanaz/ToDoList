from abc import ABC, abstractmethod
from typing import List, Optional
from src.todo_list.infrastructure.database.models.task import TaskModel

class ITaskRepository(ABC):
    @abstractmethod
    def create(self, task: TaskModel) -> TaskModel:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        pass
    
    @abstractmethod
    def get_by_project_id(self, project_id: int) -> List[TaskModel]:
        pass
    
    @abstractmethod
    def get_overdue_tasks(self) -> List[TaskModel]:
        pass
    
    @abstractmethod
    def update(self, task: TaskModel) -> TaskModel:
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass