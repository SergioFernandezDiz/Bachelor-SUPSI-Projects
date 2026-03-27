from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True)
    name = mapped_column(String(50), nullable=False)
    last_name = mapped_column(String(50), nullable=False)

    #relationships
    user_projects = relationship('UserProject', back_populates='user', lazy='selectin')#, cascade="all, delete-orphan")
    user_tasks = relationship('UserTask', back_populates='user', lazy='selectin')#, cascade="all, delete-orphan")


