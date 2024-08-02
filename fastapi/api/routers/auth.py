# For authentication
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from dotenv import load_dotenv
import os

from api.models import User
from api.deps import db_dependency, bcrypt_context

load_dotenv()

# Define router
router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)
SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM') 

class UserCreateRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
def AuthenticateUser(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return False
    
    # If user and password dont match
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def CreateAccessToken(username: str, userId: str, expiredDelta: timedelta):
    # Encode the token
    encode = {'sub': username, 'id': userId}
    expires = datetime.now(timezone.utc) + expiredDelta
    encode.update({'expires': expires.isoformat()})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint to create user
@router.post('/', status_code=status.HTTP_201_CREATED)
async def createUser(db: db_dependency, createUserRequest: UserCreateRequest):
    createUserModel = User(
        username = createUserRequest.username,
        hashed_password = bcrypt_context.hash(createUserRequest.password)
    )
    
    # Add userModel to database
    db.add(createUserModel)
    db.commit()
    
@router.post('/token', response_model=Token)
async def loginWithAccessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()], 
                               db:db_dependency):
    user = AuthenticateUser(formData.username, formData.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not authenticate user')
    
    # Create access token -> will expired in 20 minutes
    token = CreateAccessToken(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}