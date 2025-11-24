import sys
import os
sys.path.append('./src')

from sqlalchemy import create_engine
from todo_list.infrastructure.database.base import Base
from todo_list.infrastructure.database.models.project import ProjectModel
from todo_list.infrastructure.database.models.task import TaskModel

try:
    engine = create_engine('postgresql://todolist_user:todolist_pass@localhost:5432/todolist')
    Base.metadata.create_all(engine)
    print('✅ Tables created successfully!')
except Exception as e:
    print(f'❌ Error: {e}')