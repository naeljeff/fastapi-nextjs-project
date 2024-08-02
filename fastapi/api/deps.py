# For dependency

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from .database import SessionLocal

# Load data from env
load_dotenv()
SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM')

# Dependency for database
def getDbConnection():
     db = SessionLocal()
     try:
         yield db
     finally:
         db.close()
         
db_dependency = Annotated[Session, Depends(getDbConnection)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

oauth_bearer_dependency = Annotated[str, Depends(oauth_bearer)]

# GET USER
async def getCurrentUser(token: oauth_bearer_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Debugging
        username: str = payload.get('sub')
        userId: int = payload.get('id')
        
        if username is None or userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not validated')
        return {'username': username, 'userId': userId}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')


user_dependency = Annotated[dict, Depends (getCurrentUser)]
         
        
