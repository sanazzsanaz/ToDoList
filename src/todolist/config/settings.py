import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # اگر dotenv نصب نیست، از مقادیر پیش‌فرض استفاده کن
    pass

class Settings:
    MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", "10"))
    MAX_NUMBER_OF_TASKS_PER_PROJECT = int(os.getenv("MAX_NUMBER_OF_TASKS_PER_PROJECT", "50"))
    MAX_PROJECT_NAME_LENGTH = int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30"))
    MAX_PROJECT_DESCRIPTION_LENGTH = int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150"))
    MAX_TASK_TITLE_LENGTH = int(os.getenv("MAX_TASK_TITLE_LENGTH", "30"))
    MAX_TASK_DESCRIPTION_LENGTH = int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150"))

settings = Settings()