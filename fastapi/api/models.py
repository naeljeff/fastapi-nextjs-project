from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Create association tables (table tengah yang ngegabungin 2 tabel lainnya)
todo_details_association = Table(
    'todo_details', Base.metadata,
    Column('todo_details_id', Integer, ForeignKey('details.id')),
    Column('todo_master_id', Integer, ForeignKey('todo.id'))
)

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
    details = relationship('Details', secondary=todo_details_association, back_populates='todos')
    
# Class Details -> For table details
class Details(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    detail = Column(String, index=True)
    todos = relationship('Todo', secondary=todo_details_association, back_populates='details')
    
Todo.details = relationship('Details', secondary=todo_details_association, back_populates='todos')