from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import joinedload

from api.models import Todo
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    
class TodoCreate(TodoBase):
    pass

# Get specific todo id
@router.get('/{todo_id}')
def get_todo(db: db_dependency, user: user_dependency, todo_id: int):
    # Get the first id in Todo that matches
    return db.query(Todo).filter(Todo.id == todo_id ).options(joinedload(Todo.detail)).first()

# Get all todos
@router.get('/')
def get_todos(db: db_dependency, user: user_dependency):
    return db.query(Todo).options(joinedload(Todo.detail)).all()

# Create a new todo
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, user: user_dependency, todo: TodoCreate):
    # Debugging: print user to ensure it contains the 'id'
    print(f"User: {user}")
    user_id = user.get('userId')  # This should be checked
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID is missing')

    # Convert all todo into todo
    db_todo = Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    
    db.refresh(db_todo)
    return db_todo


# Delete todos
@router.delete('/{todo_id}')
def delete_todo(db: db_dependency, user: user_dependency, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo

# Update todos
@router.patch('/{todo_id}')
def update_todo(db: db_dependency, user: user_dependency, todo_id: int, updated_todo: TodoBase):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    
    # Get user id
    user_id = user.get('userId')
    # print(f"User: {user_id}")
    if existing_todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to access this todo')
    
    existing_todo.title = updated_todo.title
    existing_todo.description = updated_todo.description
    
    db.commit()
    db.refresh(existing_todo)
    
    return existing_todo