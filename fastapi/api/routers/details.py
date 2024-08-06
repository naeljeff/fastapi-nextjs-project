from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.models import Todo, Details
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix='/todos/{todo_id}/details',
    tags=['details']
)

class DetailBase(BaseModel):
    detail: str

class DetailCreate(DetailBase):
    pass

# Get detail from specific todo
@router.get('/')
def get_detail(
    todo_id: int,
    db: db_dependency,
    user: user_dependency
):
    detail_instance = db.query(Details).filter(Details.todo_id == todo_id).first()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not detail_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Detail not found')
    
    user_id = user.get('userId')
    print(f'getdetail: user_id={user_id} | todouser_id={todo.user_id}')
    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to get this todo details')
        
    return detail_instance

# Create a new detail
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_detail(
    todo_id: int,
    detail: DetailCreate,
    db: db_dependency,
    user: user_dependency
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

    user_id = user.get('userId')
    print(f'createdetail: user_id={user_id} | todouser_id={todo.user_id}')
    # print(f'UserID: {user_id} | todoUserId: {todo.user_id}')
    
    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not allowed to access this todo')

    if todo.detail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Detail already exists for this todo')

    db_detail = Details(**detail.dict(), todo_id=todo_id)
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

# Delete a specific todo's detail
@router.delete('/')
def delete_detail(
    todo_id: int, 
    db: db_dependency,
    user: user_dependency
):
    detail = db.query(Details).filter(Details.todo_id == todo_id).first()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    user_id = user.get('userId')
    print(f'deletedetail: user_id={user_id} | todouser_id={todo.user_id}')
    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to delete this todo details')
    
    if detail:
        db.delete(detail)
        db.commit()
        return {"message": "Detail deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Detail not found')

# Update specific todos detail
@router.patch('/')
def update_detail(db: db_dependency, user:user_dependency, todo_id: int, updated_detail: DetailBase):
    existing_detail = db.query(Details).filter(Details.todo_id == todo_id).first()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not existing_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Detail not found')
    
    user_id = user.get('userId')
    print(f'updatedetail: user_id={user_id} | todouser_id={todo.user_id}')
    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to edit this detail')
    
    existing_detail.detail = updated_detail.detail
    
    db.commit()
    db.refresh(existing_detail)
    
    return existing_detail