from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from .base import Base

class Task(Base):
    __tablename__ = 'task'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    location = mapped_column(String(100), nullable=False)
    start_date = mapped_column(DateTime, nullable=False)
    end_date = mapped_column(DateTime, nullable=True)
    actual_cost = mapped_column(Float, nullable=True, default=0.0)
    budget = mapped_column(Float, nullable=True, default=0.0)

    # foreign keys
    project_id = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    status = mapped_column(String(50), ForeignKey('task_status.status'), nullable=False)
    priority = mapped_column(String(20), ForeignKey('priority.level'), nullable=True)

    #relationships
    user_tasks = relationship('UserTask', back_populates='task', lazy='selectin')