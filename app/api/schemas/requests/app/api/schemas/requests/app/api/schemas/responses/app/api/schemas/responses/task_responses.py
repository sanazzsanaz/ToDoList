from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..requests.task_requests import TaskStatus

class TaskResponse(BaseModel):
    """پاسخ اطلاعات تسک"""
    id: int
    title: str
    description: str
    status: TaskStatus
    deadline: Optional[datetime]
    created_at: datetime
    project_id: int

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """پاسخ لیست تسک‌ها"""
    status: str = "success"
    data: list[TaskResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "title": "تسک نمونه",
                        "description": "توضیحات تسک",
                        "status": "todo",
                        "deadline": "2025-12-31T23:59:59",
                        "created_at": "2025-01-01T10:00:00",
                        "project_id": 1
                    }
                ],
                "total": 1
            }
        }