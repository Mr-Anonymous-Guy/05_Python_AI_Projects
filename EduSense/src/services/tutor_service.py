"""
tutor_service.py - Orchestrates AI Tutoring chat.
"""

from sqlalchemy.orm import Session
from src.storage.database import ChatHistory
from src.retrieval.rag_engine import RAGEngine

class TutorService:
    def __init__(self, db: Session, rag_engine: RAGEngine):
        self.db = db
        self.rag = rag_engine
        
    def get_chat_history(self, subject_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.subject_id == subject_id).order_by(ChatHistory.created_at.asc()).all()
        
    def ask_tutor(self, subject_id: int, message: str):
        # Save user msg
        user_msg = ChatHistory(subject_id=subject_id, role="user", content=message)
        self.db.add(user_msg)
        
        # Get history
        history = self.get_chat_history(subject_id)[-4:]
        hist_dicts = [{"role": h.role, "content": h.content} for h in history]
        
        # Query RAG
        response = self.rag.tutor_ask(subject_id, message, hist_dicts)
        
        # Save ai msg
        ai_msg = ChatHistory(subject_id=subject_id, role="assistant", content=response['answer'])
        self.db.add(ai_msg)
        self.db.commit()
        
        return response
