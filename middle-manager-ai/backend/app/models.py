from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import enum

Base = declarative_base()

class RoleEnum(enum.Enum):
    CEO = "CEO"
    MANAGER_AI = "MANAGER_AI"
    EMPLOYEE = "EMPLOYEE"

class TaskStatusEnum(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE)
    tasks = relationship("Task", back_populates="assignee")

class StrategicObjective(Base):
    __tablename__ = "objectives"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="ACTIVE")
    tasks = relationship("Task", back_populates="objective")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING)
    assignee_id = Column(Integer, ForeignKey("users.id"))
    objective_id = Column(Integer, ForeignKey("objectives.id"))
    
    assignee = relationship("User", back_populates="tasks")
    objective = relationship("StrategicObjective", back_populates="tasks")

class PerformanceLog(Base):
    __tablename__ = "performance_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    score = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# SQLite setup for MVP
SQLALCHEMY_DATABASE_URL = "sqlite:///./middle_manager.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
