<<<<<<< HEAD
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("todolist.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ایمپورت کنترلرها
from app.api.controllers import projects_controller, tasks_controller
from app.db.session import engine, Base, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    مدیریت عمر برنامه - اجرا هنگام راه‌اندازی و خاموشی
    """
    # Startup
    logger.info("🚀 Starting ToDoList API...")
    
    try:
        # ایجاد جداول دیتابیس (فقط برای توسعه)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ToDoList API...")
    try:
        # بستن اتصالات دیتابیس
        engine.dispose()
        logger.info("✅ Database connections closed successfully")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {str(e)}")

# ایجاد برنامه FastAPI
app = FastAPI(
    title="ToDoList API",
    description="""
    🎯 **سیستم مدیریت پروژه و تسک** - فاز 3
    
    یک API کامل برای مدیریت پروژه‌ها و تسک‌ها با قابلیت‌های:
    
    - ✅ ایجاد، ویرایش، حذف و مشاهده پروژه‌ها
    - ✅ ایجاد، ویرایش، حذف و مشاهده تسک‌ها
    - ✅ تغییر وضعیت تسک‌ها (todo, doing, done)
    - ✅ مدیریت ددلاین تسک‌ها
    - ✅ اعتبارسنجی پیشرفته داده‌ها
    - ✅ مستندسازی خودکار
    
    ## 🔗 لینک‌های مفید
    - [مستندات تعاملی (Swagger)](/docs)
    - [مستندات جایگزین (ReDoc)](/redoc)
    - [بررسی سلامت سرویس](/health)
    
    ## ⚠️ توجه
    رابط خط فرمان (CLI) در این نسخه منسوخ شده است.
    لطفاً از این API برای ارتباط با سیستم استفاده کنید.
    """,
    version="3.0.0",
    contact={
        "name": "تیم توسعه ToDoList",
        "email": "support@todolist.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# تنظیم CORS برای ارتباط با فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        # در محیط production دامنه‌های واقعی را اضافه کنید
    ],
    allow_credentials=True,
    allow_methods=["*"],  # تمام متدهای HTTP
    allow_headers=["*"],  # تمام هدرها
)

# اضافه کردن روترها
app.include_router(
    projects_controller.router,
    prefix="/api/v1",
    tags=["Projects"]
)

app.include_router(
    tasks_controller.router,
    prefix="/api/v1",
    tags=["Tasks"]
)

# هندلرهای خطای سراسری
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """
    هندلر خطای داخلی سرور
    """
    logger.error(f"Internal Server Error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "خطای داخلی سرور رخ داده است",
            "detail": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else "لطفاً با پشتیبانی تماس بگیرید"
        }
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    هندلر برای مسیرهای یافت نشده
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": "error",
            "message": "مسیر درخواستی یافت نشد",
            "detail": f"مسیر {request.url.path} وجود ندارد"
        }
    )

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    """
    هندلر خطای اعتبارسنجی
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "داده‌های ارسالی معتبر نیستند",
            "detail": "لطفاً مقادیر ورودی را بررسی کنید"
        }
    )

# Route های اصلی
@app.get(
    "/",
    summary="صفحه اصلی",
    description="""
    صفحه خوش‌آمدگویی و اطلاعات کلی API
    
    این endpoint اطلاعات پایه درباره API و لینک‌های مفید را ارائه می‌دهد.
    """
)
async def root():
    """
    صفحه اصلی API
    """
    return {
        "status": "success",
        "message": "🎉 خوش آمدید به ToDoList API",
        "version": "3.0.0",
        "description": "سیستم مدیریت پروژه و تسک - فاز 3 (Web API)",
        "features": [
            "مدیریت کامل پروژه‌ها و تسک‌ها",
            "اعتبارسنجی پیشرفته داده‌ها",
            "مستندسازی خودکار",
            "پاسخ‌های استاندارد RESTful"
        ],
        "links": {
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            },
            "health_check": "/health",
            "api_endpoints": {
                "projects": "/api/v1/projects",
                "tasks": "/api/v1/projects/{id}/tasks"
            }
        },
        "note": "⚠️ رابط خط فرمان (CLI) در این نسخه منسوخ شده است. لطفاً از API استفاده کنید."
    }

@app.get(
    "/health",
    summary="بررسی سلامت سرویس",
    description="""
    بررسی وضعیت سلامت و آماده‌به‌کار بودن سرویس
    
    این endpoint برای مانیتورینگ و load balancing استفاده می‌شود.
    """
)
async def health_check():
    """
    بررسی سلامت سرویس
    """
    try:
        # بررسی اتصال به دیتابیس
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "success",
            "message": "✅ سرویس در حال اجرا و سالم است",
            "database": "connected",
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "message": "❌ سرویس مشکل دارد",
                "database": "disconnected",
                "error": str(e)
            }
        )

@app.get(
    "/info",
    summary="اطلاعات فنی سرویس",
    description="""
    دریافت اطلاعات فنی و پیکربندی سرویس
    """
)
async def service_info():
    """
    اطلاعات فنی سرویس
    """
    import platform
    from sqlalchemy import text
    
    try:
        db = SessionLocal()
        db_version = db.execute(text("SELECT version()")).scalar()
        db.close()
    except Exception as e:
        db_version = f"Error: {str(e)}"
    
    return {
        "status": "success",
        "service": {
            "name": "ToDoList API",
            "version": "3.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "debug": os.getenv("DEBUG", "False").lower() == "true"
        },
        "system": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "hostname": platform.node()
        },
        "database": {
            "connected": "success" if "Error" not in db_version else "failed",
            "version": db_version if "Error" not in db_version else None
        },
        "features": {
            "cors_enabled": True,
            "auto_docs": True,
            "validation": True,
            "logging": True
        }
    }

# Route برای تست عملکرد API
@app.get(
    "/api/v1/test",
    summary="تست عملکرد API",
    description="""
    تست کلی عملکرد و پاسخ‌دهی API
    
    این endpoint برای تست سریع connectivity و response time استفاده می‌شود.
    """,
    tags=["Testing"]
)
async def test_api():
    """
    تست عملکرد API
    """
    import time
    start_time = time.time()
    
    # شبیه‌سازی یک عملیات سبک
    test_data = {
        "message": "API is working correctly",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "test_items": [
            {"id": 1, "name": "Test Project", "status": "active"},
            {"id": 2, "name": "Test Task", "status": "todo"}
        ]
    }
    
    response_time = (time.time() - start_time) * 1000  # میلی‌ثانیه
    
    return {
        "status": "success",
        "message": "✅ تست API موفقیت‌آمیز بود",
        "data": test_data,
        "performance": {
            "response_time_ms": round(response_time, 2),
            "status": "excellent" if response_time < 100 else "good"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # تنظیمات سرور از محیط یا مقادیر پیش‌فرض
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "True").lower() == "true"
    
    logger.info(f"🎯 Starting server on {host}:{port}")
    logger.info(f"📚 Documentation: http://{host}:{port}/docs")
    logger.info(f"🔍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )
=======
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from core.project import Project
from core.task import Task, TaskStatus
from core.exceptions import (
    ValidationError, DuplicateProjectError, ProjectNotFoundError,
    TaskNotFoundError, LimitExceededError
)
from storage.memory_storage import MemoryStorage

class ToDoListApp:
    def __init__(self):
        self.storage = MemoryStorage()
        self.current_project_id = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title):
        self.clear_screen()
        print("=" * 50)
        print(f"🎯 {title}")
        print("=" * 50)
    
    def wait_for_enter(self):
        input("\nPress Enter to continue...")
    
    def display_statistics(self):
        try:
            total_projects = len(self.storage.projects)
            total_tasks = len(self.storage.tasks)
            
            todo_count = 0
            doing_count = 0
            done_count = 0
            
            for task in self.storage.tasks:
                if task.status.value == "todo":
                    todo_count += 1
                elif task.status.value == "doing":
                    doing_count += 1
                elif task.status.value == "done":
                    done_count += 1
            
            completion_rate = (done_count / total_tasks * 100) if total_tasks > 0 else 0
            
            print(f"\n📊 Statistics:")
            print(f"   Projects: {total_projects} | Tasks: {total_tasks}")
            print(f"   ⏳ Todo: {todo_count} | 🔄 Doing: {doing_count} | ✅ Done: {done_count}")
            print(f"   📈 Completion Rate: {completion_rate:.1f}%")
            
        except:
            print(f"\n📊 Statistics:")
            print("   Projects: 0 | Tasks: 0")
            print("   ⏳ Todo: 0 | 🔄 Doing: 0 | ✅ Done: 0")
            print("   📈 Completion Rate: 0.0%")
    
    # Main Menu
    def main_menu(self):
        while True:
            self.display_header("ToDo List - Main Menu")
            self.display_statistics()
            
            print("\n📂 Project Management:")
            print("1. 📝 Create New Project")
            print("2. 📋 List All Projects")
            print("3. 🔍 Select Project")
            print("4. 🚪 Exit")
            
            choice = input("\n🎯 Your choice: ").strip()
            
            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.select_project()
            elif choice == "4":
                print("\n🙏 Thank you for using ToDo List! Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter number 1-4")
                self.wait_for_enter()
    
    def create_project(self):
        self.display_header("Create New Project")
        
        try:
            name = input("📛 Project name: ").strip()
            description = input("📝 Project description: ").strip()
            
            project = Project(name, description)
            created_project = self.storage.create_project(project)
            
            print(f"\n✅ Project '{created_project.name}' created successfully!")
            
        except (ValidationError, DuplicateProjectError, LimitExceededError) as e:
            print(f"\n❌ Error: {e}")
        
        self.wait_for_enter()
    
    def list_projects(self):
        self.display_header("Projects List")
        
        projects = self.storage.get_all_projects()
        if not projects:
            print("📭 No projects found")
            self.wait_for_enter()
            return
        
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project}")
        
        print(f"\n📋 Total: {len(projects)} projects")
        self.wait_for_enter()
    
    def select_project(self):
        self.display_header("Select Project")
        
        projects = self.storage.get_all_projects()
        if not projects:
            print("📭 No projects available for selection")
            self.wait_for_enter()
            return
        
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project}")
        
        try:
            choice = int(input(f"\n🎯 Select project number (1-{len(projects)}): ").strip())
            if 1 <= choice <= len(projects):
                self.current_project_id = projects[choice-1].id
                self.project_menu()
            else:
                print("❌ Invalid project number")
                self.wait_for_enter()
        except ValueError:
            print("❌ Please enter a number")
            self.wait_for_enter()
    
    # Project Menu
    def project_menu(self):
        while self.current_project_id:
            try:
                project = self.storage.get_project(self.current_project_id)
                self.display_header(f"Project: {project.name}")
                print(f"📖 {project.description}")
                
                project_tasks = [t for t in self.storage.tasks if t.project_id == self.current_project_id]
                print(f"\n📊 Project stats: {len(project_tasks)} tasks")
                
                print("\n📋 Task Management:")
                print("1. ➕ Create New Task")
                print("2. 📝 List All Tasks")
                print("3. ✏️ Edit Task")
                print("4. 🗑️ Delete Task")
                print("5. 🔄 Change Task Status")
                print("6. ⚙️ Edit Project")
                print("7. 🗑️ Delete Project")
                print("8. ↩️ Back to Main Menu")
                
                choice = input("\n🎯 Your choice: ").strip()
                
                if choice == "1":
                    self.create_task()
                elif choice == "2":
                    self.list_tasks()
                elif choice == "3":
                    self.edit_task()
                elif choice == "4":
                    self.delete_task()
                elif choice == "5":
                    self.change_task_status()
                elif choice == "6":
                    self.edit_project()
                elif choice == "7":
                    self.delete_project()
                    break
                elif choice == "8":
                    self.current_project_id = None
                else:
                    print("❌ Invalid choice!")
                    self.wait_for_enter()
                    
            except ProjectNotFoundError:
                print("❌ Project not found!")
                self.current_project_id = None
                self.wait_for_enter()
    
    def create_task(self):
        self.display_header("Create New Task")
        
        try:
            title = input("📛 Task title: ").strip()
            description = input("📝 Task description: ").strip()
            
            deadline_str = input("📅 Deadline (YYYY-MM-DD) - optional: ").strip()
            deadline = None
            if deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                except ValueError:
                    print("❌ Invalid date format! Use YYYY-MM-DD")
                    self.wait_for_enter()
                    return
            
            task = Task(title, description)
            if deadline:
                task.set_deadline(deadline)
            
            created_task = self.storage.create_task(task, self.current_project_id)
            print(f"\n✅ Task '{created_task.title}' created successfully!")
            
        except (ValidationError, LimitExceededError) as e:
            print(f"\n❌ Error: {e}")
        
        self.wait_for_enter()
    
    def list_tasks(self):
        self.display_header("Tasks List")
        
        try:
            tasks = self.storage.get_project_tasks(self.current_project_id)
            project = self.storage.get_project(self.current_project_id)
            
            print(f"📁 Project: {project.name}\n")
            
            if not tasks:
                print("📭 No tasks found in this project")
                self.wait_for_enter()
                return
            
            todo_tasks = [t for t in tasks if t.status == TaskStatus.TODO]
            doing_tasks = [t for t in tasks if t.status == TaskStatus.DOING]
            done_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
            
            if todo_tasks:
                print("⏳ Todo:")
                for task in todo_tasks:
                    print(f"   {task}")
                print()
            
            if doing_tasks:
                print("🔄 Doing:")
                for task in doing_tasks:
                    print(f"   {task}")
                print()
            
            if done_tasks:
                print("✅ Done:")
                for task in done_tasks:
                    print(f"   {task}")
                print()
            
            print(f"📊 Total: {len(tasks)} tasks")
            
        except ProjectNotFoundError as e:
            print(f"❌ {e}")
        
        self.wait_for_enter()
    
    def edit_task(self):
        self.display_header("Edit Task")
        
        try:
            tasks = self.storage.get_project_tasks(self.current_project_id)
            if not tasks:
                print("📭 No tasks available for editing")
                self.wait_for_enter()
                return
            
            print("📋 Available tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
            
            choice = int(input(f"\n🎯 Select task number to edit (1-{len(tasks)}): ").strip())
            if 1 <= choice <= len(tasks):
                task = tasks[choice-1]
                
                print(f"\n✏️ Editing task: {task.title}")
                new_title = input(f"📛 New title [{task.title}]: ").strip() or None
                new_description = input(f"📝 New description [{task.description}]: ").strip() or None
                
                current_deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else 'No deadline'
                new_deadline_str = input(f"📅 New deadline [{current_deadline}] (YYYY-MM-DD): ").strip()
                new_deadline = None
                if new_deadline_str and new_deadline_str != 'No deadline':
                    try:
                        new_deadline = datetime.strptime(new_deadline_str, "%Y-%m-%d")
                    except ValueError:
                        print("❌ Invalid date format!")
                        self.wait_for_enter()
                        return
                
                self.storage.update_task(
                    task.id,
                    title=new_title,
                    description=new_description,
                    deadline=new_deadline
                )
                print("✅ Task updated successfully!")
            else:
                print("❌ Invalid task number")
        
        except (ValueError, ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_enter()
    
    def delete_task(self):
        self.display_header("Delete Task")
        
        try:
            tasks = self.storage.get_project_tasks(self.current_project_id)
            if not tasks:
                print("📭 No tasks available for deletion")
                self.wait_for_enter()
                return
            
            print("📋 Available tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
            
            choice = int(input(f"\n🎯 Select task number to delete (1-{len(tasks)}): ").strip())
            if 1 <= choice <= len(tasks):
                task = tasks[choice-1]
                confirm = input(f"\n⚠️ Are you sure you want to delete task '{task.title}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.storage.delete_task(task.id)
                    print("✅ Task deleted successfully!")
                else:
                    print("❌ Deletion cancelled")
            else:
                print("❌ Invalid task number")
        
        except (ValueError, ProjectNotFoundError, TaskNotFoundError) as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_enter()
    
    def change_task_status(self):
        self.display_header("Change Task Status")
        
        try:
            tasks = self.storage.get_project_tasks(self.current_project_id)
            if not tasks:
                print("📭 No tasks available for status change")
                self.wait_for_enter()
                return
            
            print("📋 Available tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
            
            choice = int(input(f"\n🎯 Select task number (1-{len(tasks)}): ").strip())
            if 1 <= choice <= len(tasks):
                task = tasks[choice-1]
                
                print(f"\n🔄 Changing status for task: {task.title}")
                print(f"Current status: {task.status.value}")
                print("Available statuses: todo, doing, done")
                
                new_status = input("New status: ").strip().lower()
                self.storage.change_task_status(task.id, new_status)
                print("✅ Task status updated successfully!")
            else:
                print("❌ Invalid task number")
        
        except (ValueError, ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_enter()
    
    def edit_project(self):
        self.display_header("Edit Project")
        
        try:
            project = self.storage.get_project(self.current_project_id)
            
            print(f"✏️ Editing project: {project.name}")
            new_name = input(f"📛 New name [{project.name}]: ").strip() or None
            new_description = input(f"📝 New description [{project.description}]: ").strip() or None
            
            self.storage.update_project(self.current_project_id, new_name, new_description)
            print("✅ Project updated successfully!")
        
        except (ProjectNotFoundError, DuplicateProjectError, ValidationError) as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_enter()
    
    def delete_project(self):
        self.display_header("Delete Project")
        
        try:
            project = self.storage.get_project(self.current_project_id)
            project_tasks = [t for t in self.storage.tasks if t.project_id == self.current_project_id]
            
            confirm = input(f"⚠️ Are you sure you want to delete project '{project.name}' and all {len(project_tasks)} tasks? (y/n): ").strip().lower()
            
            if confirm == 'y':
                self.storage.delete_project(self.current_project_id)
                print("✅ Project and all its tasks deleted successfully!")
                self.current_project_id = None
            else:
                print("❌ Deletion cancelled")
        
        except ProjectNotFoundError as e:
            print(f"❌ {e}")
            self.current_project_id = None
        
        self.wait_for_enter()

def main():
    app = ToDoListApp()
    app.main_menu()

if __name__ == "__main__":
    main()
>>>>>>> 3f64151f94c84d92b417cc31d54f7ae84e9315fd
