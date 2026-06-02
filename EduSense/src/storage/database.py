"""
database.py - SQLite storage for EduSense metadata using SQLAlchemy.
"""

import os
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from src.config import DB_PATH

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    documents = relationship("Document", back_populates="subject", cascade="all, delete-orphan")
    chats = relationship("ChatHistory", back_populates="subject", cascade="all, delete-orphan")
    plans = relationship("StudyPlan", back_populates="subject", cascade="all, delete-orphan")
    quizzes = relationship("QuizResult", back_populates="subject", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)
    num_chunks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subject = relationship("Subject", back_populates="documents")

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    role = Column(String(50), nullable=False) # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subject = relationship("Subject", back_populates="chats")

class StudyPlan(Base):
    __tablename__ = 'study_plans'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    plan_type = Column(String(50), nullable=False) # 'weekly', 'daily', 'exam'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subject = relationship("Subject", back_populates="plans")

class QuizResult(Base):
    __tablename__ = 'quiz_results'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    score = Column(Float, nullable=False)
    weak_topics = Column(Text, nullable=True) # JSON array of strings
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subject = relationship("Subject", back_populates="quizzes")

# Setup engine and session
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database schema."""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
