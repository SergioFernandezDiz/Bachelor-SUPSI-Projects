from sqlalchemy import Integer, String,ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Project(Base):
    __tablename__ = 'project'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)

    #foreign keys
    project_type = mapped_column(String(50), ForeignKey('project_type.type'), nullable=False)
    project_status = mapped_column(String(50), ForeignKey('project_status.status'), nullable=False)


    #relationships
    tasks = relationship('Task', backref='project', lazy='selectin') #backref not permits to manage the inverse relation
    user_projects = relationship('UserProject', back_populates='project', lazy='selectin') #backpop permits to manage the inverse relation

