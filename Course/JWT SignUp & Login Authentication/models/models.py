from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()
class User(base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,  index=True , nullable=False)
    email = Column(String,  index=True , nullable=False)
    password = Column(String , nullable=False)
    