from sqlalchemy import String,Text
from sqlalchemy.orm import mapped_column
from .base import Base

# role of a user in a project
class Role(Base):
    __tablename__ = 'role'
    name = mapped_column(String(50), primary_key=True)
    description = mapped_column(Text, nullable=True)