from fastapi import FastAPI
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# ایجاد برنامه FastAPI
app = FastAPI(
    title="ToDoList API - NEW VERSION",
    description="سیستم مدیریت پروژه و تسک - نسخه جدید",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "🎉 خوش آمدید به ToDoList API - نسخه جدید!",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "سرویس جدید در حال اجراست"}

@app.get("/test")
async def test():
    return {"message": "این نسخه جدید API است"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )