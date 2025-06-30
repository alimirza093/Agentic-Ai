from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False) 
    datetime = Column(String, index=True , default= datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nullable = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="todos") 


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True , nullable=False)
    username = Column(String, unique=True, index=True , nullable=False)
    email = Column(String, unique=True, index=True , nullable=False)
    password = Column(String , nullable = False)

    todos = relationship("Todo", back_populates="user")  
