from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from datetime import datetime
import enum
from src.todo_list.infrastructure.database.base import Base

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), nullable=False)
    description = Column(String(150), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))