from .database import Base
from sqlalchemy import Column,Integer, String, Boolean
class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    email = Column (String, nullable=False, unique=True)
    password = Column(String, nullable=False)