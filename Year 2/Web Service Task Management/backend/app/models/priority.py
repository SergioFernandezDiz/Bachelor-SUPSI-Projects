from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from .base import Base

class Priority(Base):
    __tablename__ = 'priority'
    level = mapped_column(String(20), primary_key=True)