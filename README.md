ToDoList Project
A task and project management system developed in four phases. This project is implemented with layered architecture and software engineering principles.

Project Introduction
This project is a complete task management system that includes features for creating projects, managing tasks, status changes, and automatic scheduling. The project was developed gradually in four phases.

Development Phases
Phase 1: Basic Implementation
Object-Oriented Architecture with Python

Temporary in-memory storage

Project and task management

Data validation and error handling

Phase 2: Database and Scheduling
Migration to PostgreSQL database

SQLAlchemy ORM implementation

Repository pattern implementation

Automatic scheduling for closing overdue tasks

Database migration management with Alembic

Phase 3: API Interface
REST API development with FastAPI

Automatic documentation with Swagger UI

Advanced validation with Pydantic

Complete layered architecture

Phase 4: Testing and Documentation
Complete Postman test collection

Configurable testing environments

Comprehensive API testing guide

Complete technical documentation

Main Features
Project creation and management

Adding and editing tasks within projects

Task status changes (todo, doing, done)

Setting task deadlines

Cascading deletion of projects and related tasks

Input data validation

System error handling

Automatic API documentation

Comprehensive testing

Technologies Used
Python 3.8+

FastAPI

SQLAlchemy ORM

PostgreSQL

Pydantic

Alembic

Docker

Poetry

Postman

Project Structure
text
todolist/
├── app/
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   └── db/
├── postman/
├── tests/
├── docker-compose.yml
├── pyproject.toml
└── README.md
Setup
Prerequisites
Python 3.8 or higher

Docker and Docker Compose

Poetry

Installation and Running
Clone the repository:

bash
git clone https://github.com/sanazzsanaz/ToDoList.git
cd ToDoList
Install dependencies:

bash
poetry install
Set up the database:

bash
docker-compose up -d
Run the application:

bash
uvicorn main:app --reload
Access the API:

API: http://localhost:8000

Documentation: http://localhost:8000/docs

Health check: http://localhost:8000/health

Testing with Postman
For complete API testing, you can use the Postman collection:

Import the postman/todolist-collection.json file in Postman

Import the postman/todolist-environment.json file as Environment

Select the "ToDoList Dev" environment

Execute requests in order

Architecture
This project was developed with layered architecture:

Controller Layer: HTTP request management

Service Layer: Business logic

Repository Layer: Data access

Model Layer: Database entities

Developers
This project was developed as part of the Software Engineering course at Amirkabir University of Technology.

License
This project was developed for educational purposes.
