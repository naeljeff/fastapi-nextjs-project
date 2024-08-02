from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter 
from sqlalchemy.orm import joinedload 

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