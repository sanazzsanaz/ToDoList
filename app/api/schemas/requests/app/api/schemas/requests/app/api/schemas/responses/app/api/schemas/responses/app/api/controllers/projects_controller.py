from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.project_service import ProjectService
from app.api.schemas.requests.project_requests import ProjectCreateRequest, ProjectUpdateRequest
from app.api.schemas.responses.project_responses import ProjectResponse, ProjectDetailResponse, ProjectListResponse

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    دریافت لیست تمام پروژه‌ها
    
    - **skip**: تعداد رکوردهایی که باید رد شوند (برای صفحه‌بندی)
    - **limit**: حداکثر تعداد رکوردهای بازگشتی
    """
    try:
        project_service = ProjectService(db)
        projects = project_service.get_all_projects(skip=skip, limit=limit)
        total = project_service.get_projects_count()
        
        return ProjectListResponse(
            data=projects,
            total=total
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreateRequest,
    db: Session = Depends(get_db)
):
    """
    ایجاد پروژه جدید
    
    - **name**: نام پروژه (حداکثر 30 کاراکتر)
    - **description**: توضیحات پروژه (حداکثر 150 کاراکتر)
    """
    try:
        project_service = ProjectService(db)
        project = project_service.create_project(
            name=project_data.name,
            description=project_data.description
        )
        return project
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

@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    دریافت اطلاعات یک پروژه بر اساس شناسه
    
    - **project_id**: شناسه پروژه
    """
    try:
        project_service = ProjectService(db)
        project = project_service.get_project_by_id(project_id)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
            
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    ویرایش کامل اطلاعات پروژه
    
    - **project_id**: شناسه پروژه
    - **name**: نام جدید پروژه
    - **description**: توضیحات جدید پروژه
    """
    try:
        project_service = ProjectService(db)
        
        # بررسی وجود پروژه
        existing_project = project_service.get_project_by_id(project_id)
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
        
        updated_project = project_service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        
        return updated_project
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

@router.patch("/{project_id}", response_model=ProjectResponse)
async def partial_update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    ویرایش جزئی اطلاعات پروژه
    
    - **project_id**: شناسه پروژه
    - **name**: نام جدید پروژه (اختیاری)
    - **description**: توضیحات جدید پروژه (اختیاری)
    """
    try:
        project_service = ProjectService(db)
        
        # بررسی وجود پروژه
        existing_project = project_service.get_project_by_id(project_id)
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
        
        # فقط فیلدهای ارسال شده را آپدیت کن
        update_data = {}
        if project_data.name is not None:
            update_data['name'] = project_data.name
        if project_data.description is not None:
            update_data['description'] = project_data.description
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="هیچ داده‌ای برای ویرایش ارسال نشده است"
            )
        
        updated_project = project_service.update_project(
            project_id=project_id,
            **update_data
        )
        
        return updated_project
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

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    حذف پروژه
    
    - **project_id**: شناسه پروژه
    """
    try:
        project_service = ProjectService(db)
        
        # بررسی وجود پروژه
        existing_project = project_service.get_project_by_id(project_id)
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="پروژه مورد نظر یافت نشد"
            )
        
        project_service.delete_project(project_id)
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطای سرور: {str(e)}"
        )