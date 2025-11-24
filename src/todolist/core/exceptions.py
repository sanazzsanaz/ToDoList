class ToDoListException(Exception):
    """Base exception for ToDoList application"""
    pass

class ValidationError(ToDoListException):
    """Raised when validation fails"""
    pass

class DuplicateProjectError(ToDoListException):
    """Raised when project name is duplicate"""
    pass

class ProjectNotFoundError(ToDoListException):
    """Raised when project is not found"""
    pass

class TaskNotFoundError(ToDoListException):
    """Raised when task is not found"""
    pass

class LimitExceededError(ToDoListException):
    """Raised when maximum limits are exceeded"""
    pass