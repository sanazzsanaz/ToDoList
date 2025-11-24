from typing import List, Optional
from sqlalchemy.orm import Session
from ...interfaces.repositories.project_repo import IProjectRepository
from ...core.models.project import Project
from ..database.models.project import ProjectModel

class SQLAlchemyProjectRepository(IProjectRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, project: Project) -> Project:
        project_model = ProjectModel(
            name=project.name,
            description=project.description
        )
        self.session.add(project_model)
        self.session.flush()
        
        # تبدیل به مدل دامنه
        return Project(
            id=project_model.id,
            name=project_model.name,
            description=project_model.description,
            created_at=project_model.created_at
        )
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        project_model = self.session.query(ProjectModel).filter(ProjectModel.id == project_id).first()
        if project_model:
            return Project(
                id=project_model.id,
                name=project_model.name,
                description=project_model.description,
                created_at=project_model.created_at
            )
        return None
    
    # سایر متدها...