from datetime import datetime
from enum import Enum
from .exceptions import ValidationError
from config.settings import settings

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task:
    def __init__(self, title: str, description: str, project_id: int = None):
        self._validate_title(title)
        self._validate_description(description)
        
        self.id = None
        self.title = title
        self.description = description
        self.status = TaskStatus.TODO
        self.deadline = None
        self.project_id = project_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _validate_title(self, title: str):
        if not title or not title.strip():
            raise ValidationError("عنوان تسک نمی‌تواند خالی باشد")
        if len(title) > settings.MAX_TASK_TITLE_LENGTH:
            raise ValidationError(f"عنوان تسک نمی‌تواند بیشتر از {settings.MAX_TASK_TITLE_LENGTH} کاراکتر باشد")
    
    def _validate_description(self, description: str):
        if not description or not description.strip():
            raise ValidationError("توضیحات تسک نمی‌تواند خالی باشد")
        if len(description) > settings.MAX_TASK_DESCRIPTION_LENGTH:
            raise ValidationError(f"توضیحات تسک نمی‌تواند بیشتر از {settings.MAX_TASK_DESCRIPTION_LENGTH} کاراکتر باشد")
    
    def update(self, title: str = None, description: str = None, status: str = None, deadline: datetime = None):
        if title is not None:
            self._validate_title(title)
            self.title = title
        
        if description is not None:
            self._validate_description(description)
            self.description = description
        
        if status is not None:
            self.set_status(status)
        
        if deadline is not None:
            self.set_deadline(deadline)
        
        self.updated_at = datetime.now()
    
    def set_status(self, status: str):
        try:
            self.status = TaskStatus(status)
        except ValueError:
            raise ValidationError(f"وضعیت باید یکی از موارد باشد: {', '.join([s.value for s in TaskStatus])}")
    
    def set_deadline(self, deadline: datetime):
        if deadline and deadline < datetime.now():
            raise ValidationError("ددلاین نمی‌تواند در گذشته باشد")
        self.deadline = deadline
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'project_id': self.project_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        status_emoji = {
            TaskStatus.TODO: "⏳",
            TaskStatus.DOING: "🔄", 
            TaskStatus.DONE: "✅"
        }
        deadline_str = f" | 📅 {self.deadline.strftime('%Y-%m-%d')}" if self.deadline else ""
        return f"{status_emoji[self.status]} {self.title}{deadline_str}"