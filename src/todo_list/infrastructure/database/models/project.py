from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.todo_list.infrastructure.database.base import Base

class ProjectModel(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False, index=True)
    description = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)