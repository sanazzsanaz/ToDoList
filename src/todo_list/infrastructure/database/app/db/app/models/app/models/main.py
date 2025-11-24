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

# ایمپورت مدل‌ها و session
from app.db.session import Base, engine, SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    مدیریت عمر برنامه - اجرا هنگام راه‌اندازی و خاموشی
    """
    # Startup
    logger.info("🚀 Starting ToDoList API...")
    
    try:
        # ایجاد جداول دیتابیس
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

# ایمپورت و اضافه کردن روترها
try:
    from app.api.controllers.projects_controller import router as projects_router
    from app.api.controllers.tasks_controller import router as tasks_controller
    
    app.include_router(projects_router, prefix="/api/v1", tags=["Projects"])
    app.include_router(tasks_router, prefix="/api/v1", tags=["Tasks"])
    
    logger.info("✅ API routers loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️ Some routers not available: {e}")

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