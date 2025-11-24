from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """وضعیت‌های ممکن برای تسک"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class TaskCreateRequest(BaseModel):
    """درخواست ایجاد تسک جدید"""
    title: str = Field(..., min_length=1, max_length=30, description="عنوان تسک (حداکثر 30 کاراکتر)")
    description: str = Field(..., min_length=1, max_length=150, description="توضیحات تسک (حداکثر 150 کاراکتر)")
    deadline: Optional[datetime] = Field(None, description="ددلاین تسک")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="وضعیت تسک")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "تسک نمونه",
                "description": "این یک تسک نمونه برای تست است",
                "deadline": "2025-12-31T23:59:59",
                "status": "todo"
            }
        }

class TaskUpdateRequest(BaseModel):
    """درخواست ویرایش تسک"""
    title: Optional[str] = Field(None, min_length=1, max_length=30, description="عنوان تسک")
    description: Optional[str] = Field(None, min_length=1, max_length=150, description="توضیحات تسک")
    deadline: Optional[datetime] = Field(None, description="ددلاین تسک")
    status: Optional[TaskStatus] = Field(None, description="وضعیت تسک")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "تسک ویرایش شده",
                "description": "توضیحات ویرایش شده تسک",
                "status": "doing"
            }
        }