from typing import List, Optional
from ...core.models.project import Project
from ...interfaces.repositories.project_repo import IProjectRepository
from ...core.exceptions.service_exceptions import ProjectAlreadyExistsError, ProjectNotFoundError

class ProjectService:
    def __init__(self, project_repository: IProjectRepository):
        self.project_repo = project_repository
    
    def create_project(self, name: str, description: str) -> Project:
        # بررسی تکراری نبودن نام
        existing_project = self.project_repo.get_by_name(name)
        if existing_project:
            raise ProjectAlreadyExistsError(f"Project with name '{name}' already exists")
        
        # ایجاد پروژه جدید
        project = Project(name=name, description=description)
        return self.project_repo.create(project)
    
    def get_project(self, project_id: int) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with id {project_id} not found")
        return project
    
    # سایر متدهای سرویس...