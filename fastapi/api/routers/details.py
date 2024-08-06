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

@router.get('/')
def get_detail(
    todo_id: int,
    db: Session = Depends(db_dependency),
    user: dict = Depends(user_dependency)
):
    detail_instance = db.query(Details).filter(Details.todo_id == todo_id).first()

    if not detail_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Detail not found')
    return detail_instance

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_detail(
    todo_id: int, 
    detail: DetailCreate, 
    db: Session = Depends(db_dependency), 
    user: dict = Depends(user_dependency)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
    if todo.detail:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Detail already exists for this todo')

    db_detail = Details(**detail.dict(), todo_id=todo_id)
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

@router.delete('/')
def delete_detail(
    todo_id: int, 
    db: Session = Depends(db_dependency), 
    user: dict = Depends(user_dependency)
):
    detail = db.query(Details).filter(Details.todo_id == todo_id).first()

    if detail:
        db.delete(detail)
        db.commit()
        return {"message": "Detail deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Detail not found')
