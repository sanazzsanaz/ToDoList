from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.api.schemas.requests.task_requests import TaskCreateRequest, TaskUpdateRequest
from app.api.schemas.responses.task_responses import TaskResponse, TaskListResponse

router = APIRouter(prefix="/api/v1", tags=["Tasks"])

@router.get("/projects/{project_id}/tasks", response_model=TaskListResponse)
async def list_project_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    دریافت لیست تمام تسک‌های یک پروژه
    
    - **project_id**: شناسه پروژه
    - **skip**: تعداد رکوردهایی که باید رد شوند
    - **limit**: حداکثر تعداد رکوردهای بازگشتی
    """
    try:
        # بررسی وجود پروژه
        project_service = ProjectService(db)
        project = project_service.get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
        
        task_service = TaskService(db)
        tasks = task_service.get_tasks_by_project(project_id, skip=skip, limit=limit)
        total = task_service.get_tasks_count_by_project(project_id)
        
        return TaskListResponse(
            data=tasks,
            total=total
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: int,
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db)
):
    """
    ایجاد تسک جدید در یک پروژه
    
    - **project_id**: شناسه پروژه
    - **title**: عنوان تسک (حداکثر 30 کاراکتر)
    - **description**: توضیحات تسک (حداکثر 150 کاراکتر)
    - **deadline**: ددلاین تسک (اختیاری)
    - **status**: وضعیت تسک (پیش‌فرض: todo)
    """
    try:
        # بررسی وجود پروژه
        project_service = ProjectService(db)
        project = project_service.get_project_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
        
        task_service = TaskService(db)
        task = task_service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            status=task_data.status
        )
        
        return task
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    دریافت اطلاعات یک تسک بر اساس شناسه
    
    - **task_id**: شناسه تسک
    """
    try:
        task_service = TaskService(db)
        task = task_service.get_task_by_id(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="تسک مورد نظر یافت نشد"
            )
            
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    ویرایش کامل اطلاعات تسک
    
    - **task_id**: شناسه تسک
    - **title**: عنوان جدید تسک
    - **description**: توضیحات جدید تسک
    - **deadline**: ددلاین جدید تسک
    - **status**: وضعیت جدید تسک
    """
    try:
        task_service = TaskService(db)
        
        # بررسی وجود تسک
        existing_task = task_service.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="تسک مورد نظر یافت نشد"
            )
        
        updated_task = task_service.update_task(
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline,
            status=task_data.status
        )
        
        return updated_task
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def partial_update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    ویرایش جزئی اطلاعات تسک
    
    - **task_id**: شناسه تسک
    - **title**: عنوان جدید تسک (اختیاری)
    - **description**: توضیحات جدید تسک (اختیاری)
    - **deadline**: ددلاین جدید تسک (اختیاری)
    - **status**: وضعیت جدید تسک (اختیاری)
    """
    try:
        task_service = TaskService(db)
        
        # بررسی وجود تسک
        existing_task = task_service.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="تسک مورد نظر یافت نشد"
            )
        
        # فقط فیلدهای ارسال شده را آپدیت کن
        update_data = {}
        if task_data.title is not None:
            update_data['title'] = task_data.title
        if task_data.description is not None:
            update_data['description'] = task_data.description
        if task_data.deadline is not None:
            update_data['deadline'] = task_data.deadline
        if task_data.status is not None:
            update_data['status'] = task_data.status
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="هیچ داده‌ای برای ویرایش ارسال نشده است"
            )
        
        updated_task = task_service.update_task(
            task_id=task_id,
            **update_data
        )
        
        return updated_task
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_data: TaskUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    تغییر وضعیت تسک
    
    - **task_id**: شناسه تسک
    - **status**: وضعیت جدید تسک
    """
    try:
        task_service = TaskService(db)
        
        # بررسی وجود تسک
        existing_task = task_service.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="تسک مورد نظر یافت نشد"
            )
        
        if status_data.status is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="وضعیت جدید ارسال نشده است"
            )
        
        updated_task = task_service.update_task_status(
            task_id=task_id,
            status=status_data.status
        )
        
        return updated_task
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    حذف تسک
    
    - **task_id**: شناسه تسک
    """
    try:
        task_service = TaskService(db)
        
        # بررسی وجود تسک
        existing_task = task_service.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="تسک مورد نظر یافت نشد"
            )
        
        task_service.delete_task(task_id)
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )