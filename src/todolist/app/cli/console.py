import warnings
from typing import Optional
from datetime import datetime

def show_deprecation_warning():
    """
    نمایش هشدار منسوخ شدن CLI
    """
    warnings.warn(
        "⚠️  WARNING: CLI interface is deprecated and will be removed in the next release. "
        "Please use the FastAPI HTTP interface instead.",
        DeprecationWarning,
        stacklevel=2
    )
    print("=" * 80)
    print("⚠️  WARNING: CLI interface is deprecated!")
    print("This command-line interface will be removed in the next release.")
    print("Please use the FastAPI HTTP interface instead.")
    print("Run: uvicorn main:app --reload")
    print("Then visit: http://localhost:8000/docs")
    print("=" * 80)

def create_project_cli(name: str, description: str):
    """
    ایجاد پروژه از طریق CLI (منسوخ شده)
    """
    show_deprecation_warning()
    # منطق قدیمی...
    print(f"Creating project: {name}")

def list_projects_cli():
    """
    نمایش لیست پروژه‌ها از طریق CLI (منسوخ شده)
    """
    show_deprecation_warning()
    # منطق قدیمی...
    print("Listing projects...")

# سایر توابع CLI با هشدار مشابه...