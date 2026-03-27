from sqlalchemy import  String, Text
from sqlalchemy.orm import mapped_column
from .base import Base

class ProjectStatus(Base):
    __tablename__ = 'project_status'
    status = mapped_column(String(50), primary_key=True)
    description = mapped_column(Text, nullable=True) #String(200)

class TaskStatus(Base):
    __tablename__ = 'task_status'
    status = mapped_column(String(50), primary_key=True)
    description = mapped_column(Text, nullable=True)  # String(200)