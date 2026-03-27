from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column
from .base import Base

class ProjectType(Base):
    __tablename__ = 'project_type'
    type = mapped_column(String(50), primary_key=True)
    description = mapped_column(Text, nullable=True) #String(200)