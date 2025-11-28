# ToDo List - Python OOP Project

A simple ToDo List application built with Python OOP and in-memory storage.

## Features
- Project management (Create, Read, Update, Delete)
- Task management with status tracking
- English CLI interface
- Input validation and error handling

## Setup
1. Install dependencies: `poetry install`
2. Run: `poetry run python src/todolist/main.py`

## Phase 1
In-memory storage implementation with OOP architecture.

## 🚀 API Testing with Postman

This project includes a complete Postman collection for testing all API endpoints.

### Quick Start:
1. Import the collection from `postman/todolist-collection.json`
2. Import the environment from `postman/todolist-environment.json` 
3. Select 'ToDoList Dev' environment in Postman
4. Start server: `docker-compose up -d`
5. Run requests in the organized collection

### Collection Structure:
- **Health Check**: API status verification
- **Projects**: Project management operations
- **Tasks**: Task management within projects

See [postman/README.md](postman/README.md) for detailed instructions.
