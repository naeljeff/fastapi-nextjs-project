from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Class User -> For table user
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    

# Class Todo -> For table todo
class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, index=True)
    description = Column(String, index=True)
    detail = relationship('Details', back_populates='todo', uselist=False)
    
# Class Details -> For table details
class Details(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey('todo.id'), unique=True)
    detail = Column(String, index=True)
    todo = relationship('Todo', back_populates='detail')