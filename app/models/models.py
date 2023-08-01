from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from config.dbconnection import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(256))
    task_type = Column(String(20))
    assignee = Column(String(45))
    task_status = Column(String(45))
    comments = Column(String(256))
    created_date = Column(String(50))
    updated_date = Column(String(50))


class ArchiveTask(Base):
    __tablename__ = "archive_task"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(256))
    task_type = Column(String(20))
    assignee = Column(String(45))
    task_status = Column(String(45))
    comments = Column(String(256))
    created_date = Column(String(50))
    updated_date = Column(String(50))
