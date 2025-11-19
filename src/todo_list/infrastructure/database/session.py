from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# ایجاد engine
engine = create_engine('postgresql://todolist_user:todolist_pass@localhost:5432/todolist')

# ایجاد session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """ایجاد session برای دیتابیس"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()