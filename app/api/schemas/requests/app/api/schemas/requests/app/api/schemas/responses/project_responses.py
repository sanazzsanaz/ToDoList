from pydantic import BaseModel
from datetime import datetime
from typing import List
from .task_responses import TaskResponse

class ProjectResponse(BaseModel):
    """پاسخ اطلاعات پروژه"""
    id: int
    name: str
    description: str
    created_at: datetime
    tasks_count: int

    class Config:
        from_attributes = True

class ProjectDetailResponse(ProjectResponse):
    """پاسخ جزئیات کامل پروژه همراه با تسک‌ها"""
    tasks: List[TaskResponse]

class ProjectListResponse(BaseModel):
    """پاسخ لیست پروژه‌ها"""
    status: str = "success"
    data: List[ProjectResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "پروژه نمونه",
                        "description": "توضیحات پروژه",
                        "created_at": "2025-01-01T10:00:00",
                        "tasks_count": 5
                    }
                ],
                "total": 1
            }
        }