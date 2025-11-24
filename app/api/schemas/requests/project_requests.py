from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectCreateRequest(BaseModel):
    """درخواست ایجاد پروژه جدید"""
    name: str = Field(..., min_length=1, max_length=30, description="نام پروژه (حداکثر 30 کاراکتر)")
    description: str = Field(..., min_length=1, max_length=150, description="توضیحات پروژه (حداکثر 150 کاراکتر)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "پروژه نمونه",
                "description": "این یک پروژه نمونه برای تست است"
            }
        }

class ProjectUpdateRequest(BaseModel):
    """درخواست ویرایش پروژه"""
    name: Optional[str] = Field(None, min_length=1, max_length=30, description="نام پروژه (حداکثر 30 کاراکتر)")
    description: Optional[str] = Field(None, min_length=1, max_length=150, description="توضیحات پروژه (حداکثر 150 کاراکتر)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "پروژه ویرایش شده",
                "description": "توضیحات ویرایش شده پروژه"
            }
        }