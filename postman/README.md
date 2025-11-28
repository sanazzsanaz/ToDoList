# Postman Testing Guide

## Collection Import
1. Open Postman
2. Click Import → Select 'todolist-collection.json'
3. Click Import

## Environment Setup  
1. Go to Environments → Import
2. Select 'todolist-environment.json'
3. Select 'ToDoList Dev' from environment dropdown

## Testing Sequence
1. Health Check - Verify API is running
2. Create Project - Test project creation
3. Get Projects - Test project retrieval

## Environment Variables
- base_url: http://localhost:8000
- api_version: v1
- project_id: (auto-set during tests)
- task_id: (auto-set during tests)

## Prerequisites
- Ensure FastAPI server is running on http://localhost:8000
- Database should be available via docker-compose
