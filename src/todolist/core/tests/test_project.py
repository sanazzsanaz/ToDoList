import pytest
from src.todolist.core.project import Project
from src.todolist.core.exceptions import ValidationError
from src.todolist.storage.memory_storage import MemoryStorage

class TestProject:
    def test_create_project_valid(self):
        project = Project("Test Project", "Test Description")
        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.id is None
    
    def test_create_project_invalid_name(self):
        with pytest.raises(ValidationError):
            Project("", "Test Description")
        
        with pytest.raises(ValidationError):
            Project("A" * 31, "Test Description")
    
    def test_project_update(self):
        project = Project("Test Project", "Test Description")
        project.update("New Name", "New Description")
        assert project.name == "New Name"
        assert project.description == "New Description"

class TestProjectStorage:
    def test_create_project_in_storage(self):
        storage = MemoryStorage()
        project = Project("Test Project", "Test Description")
        created_project = storage.create_project(project)
        
        assert created_project.id == 1
        assert len(storage.projects) == 1
    
    def test_duplicate_project_name(self):
        storage = MemoryStorage()
        project1 = Project("Test Project", "Test Description")
        project2 = Project("Test Project", "Another Description")
        
        storage.create_project(project1)
        with pytest.raises(Exception):  # Should raise DuplicateProjectError
            storage.create_project(project2)