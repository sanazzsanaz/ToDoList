from datetime import datetime
from .exceptions import ValidationError
from config.settings import settings

class Project:
    def __init__(self, name: str, description: str):
        self._validate_name(name)
        self._validate_description(description)
        
        self.id = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks = []
    
    def _validate_name(self, name: str):
        if not name or not name.strip():
            raise ValidationError("نام پروژه نمی‌تواند خالی باشد")
        if len(name) > settings.MAX_PROJECT_NAME_LENGTH:
            raise ValidationError(f"نام پروژه نمی‌تواند بیشتر از {settings.MAX_PROJECT_NAME_LENGTH} کاراکتر باشد")
    
    def _validate_description(self, description: str):
        if not description or not description.strip():
            raise ValidationError("توضیحات پروژه نمی‌تواند خالی باشد")
        if len(description) > settings.MAX_PROJECT_DESCRIPTION_LENGTH:
            raise ValidationError(f"توضیحات پروژه نمی‌تواند بیشتر از {settings.MAX_PROJECT_DESCRIPTION_LENGTH} کاراکتر باشد")
    
    def update(self, name: str = None, description: str = None):
        if name is not None:
            self._validate_name(name)
            self.name = name
        
        if description is not None:
            self._validate_description(description)
            self.description = description
        
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'task_count': len(self.tasks),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self):
        return f"📁 {self.name} ({len(self.tasks)} تسک)"