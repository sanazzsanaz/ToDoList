from typing import List, Optional
from datetime import datetime
from core.project import Project
from core.task import Task, TaskStatus
from core.exceptions import (
    DuplicateProjectError, ProjectNotFoundError, TaskNotFoundError, 
    LimitExceededError, ValidationError
)
from config.settings import settings

class MemoryStorage:
    def __init__(self):
        self.projects: List[Project] = []
        self.tasks: List[Task] = []
        self.next_project_id = 1
        self.next_task_id = 1
    
    # Project Methods
    def create_project(self, project: Project) -> Project:
        if len(self.projects) >= settings.MAX_NUMBER_OF_PROJECTS:
            raise LimitExceededError(f"تعداد پروژه‌ها نمی‌تواند بیشتر از {settings.MAX_NUMBER_OF_PROJECTS} باشد")
        
        if any(p.name == project.name for p in self.projects):
            raise DuplicateProjectError(f"پروژه با نام '{project.name}' از قبل وجود دارد")
        
        project.id = self.next_project_id
        self.next_project_id += 1
        self.projects.append(project)
        return project
    
    def get_project(self, project_id: int) -> Project:
        project = next((p for p in self.projects if p.id == project_id), None)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد")
        return project
    
    def get_all_projects(self) -> List[Project]:
        return sorted(self.projects, key=lambda p: p.created_at)
    
    def update_project(self, project_id: int, name: str = None, description: str = None) -> Project:
        project = self.get_project(project_id)
        
        if name and any(p.name == name and p.id != project_id for p in self.projects):
            raise DuplicateProjectError(f"پروژه با نام '{name}' از قبل وجود دارد")
        
        project.update(name, description)
        return project
    
    def delete_project(self, project_id: int) -> bool:
        project = self.get_project(project_id)
        
        # Cascade delete tasks
        project_tasks = [t for t in self.tasks if t.project_id == project_id]
        for task in project_tasks:
            self.tasks.remove(task)
        
        self.projects.remove(project)
        return True
    
    # Task Methods
    def create_task(self, task: Task, project_id: int) -> Task:
        project = self.get_project(project_id)
        
        project_tasks = [t for t in self.tasks if t.project_id == project_id]
        if len(project_tasks) >= settings.MAX_NUMBER_OF_TASKS_PER_PROJECT:
            raise LimitExceededError(f"تعداد تسک‌های هر پروژه نمی‌تواند بیشتر از {settings.MAX_NUMBER_OF_TASKS_PER_PROJECT} باشد")
        
        task.id = self.next_task_id
        task.project_id = project_id
        self.next_task_id += 1
        self.tasks.append(task)
        return task
    
    def get_task(self, task_id: int) -> Task:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} یافت نشد")
        return task
    
    def get_project_tasks(self, project_id: int) -> List[Task]:
        self.get_project(project_id)  # Validate project exists
        project_tasks = [t for t in self.tasks if t.project_id == project_id]
        return sorted(project_tasks, key=lambda t: t.created_at)
    
    def update_task(self, task_id: int, **kwargs) -> Task:
        task = self.get_task(task_id)
        task.update(**kwargs)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        self.tasks.remove(task)
        return True
    
    def change_task_status(self, task_id: int, status: str) -> Task:
        task = self.get_task(task_id)
        task.set_status(status)
        task.updated_at = datetime.now()
        return task
    
    # Statistics - این متد رو اضافه کردم
    def get_statistics(self) -> dict:
        """آمار کلی سیستم رو برمی‌گرداند"""
        total_tasks = len(self.tasks)
        todo_tasks = len([t for t in self.tasks if t.status.value == "todo"])
        doing_tasks = len([t for t in self.tasks if t.status.value == "doing"])
        done_tasks = len([t for t in self.tasks if t.status.value == "done"])
        
        completion_rate = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_projects': len(self.projects),
            'total_tasks': total_tasks,
            'todo_tasks': todo_tasks,
            'doing_tasks': doing_tasks,
            'done_tasks': done_tasks,
            'completion_rate': completion_rate
        }