from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class UserProject(Base):
    __tablename__ = 'user_project'
    user_id = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey('project.id'), primary_key=True)

    #relationships
    user = relationship('User', back_populates='user_projects')
    project = relationship('Project', back_populates='user_projects')

    # foreign keys
    role = mapped_column(String(50), ForeignKey('role.name'), nullable=True)

class UserTask(Base):
    __tablename__ = 'user_task'
    user_id = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
    task_id = mapped_column(Integer, ForeignKey('task.id'), primary_key=True)
    work_hours = mapped_column(Float, nullable=True, default=0)

    #relationships
    user = relationship('User', back_populates='user_tasks')
    task = relationship('Task', back_populates='user_tasks')
