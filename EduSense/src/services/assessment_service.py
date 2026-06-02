"""
assessment_service.py - Flashcards, Quizzes, and Analytics routing.
"""

import json
from sqlalchemy.orm import Session
from src.storage.database import QuizResult
from src.ai.llm_manager import LLMManager
from src.storage.faiss_manager import FaissManager
from src.analytics.analytics_engine import AnalyticsEngine
from langchain_core.messages import SystemMessage, HumanMessage

class AssessmentService:
    def __init__(self, db: Session, llm: LLMManager, faiss: FaissManager):
        self.db = db
        self.llm = llm
        self.faiss = faiss
        self.analytics = AnalyticsEngine(llm)
        
    def _get_subject_context(self, subject_id: int) -> str:
        vectorstore = self.faiss.load_vectorstore(subject_id)
        if not vectorstore: return ""
        docs = vectorstore.as_retriever(search_kwargs={"k": 20}).invoke("core concepts overview")
        return "\n".join([d.page_content for d in docs])
        
    def generate_flashcards(self, subject_id: int) -> str:
        context = self._get_subject_context(subject_id)
        if not context: return "Please upload documents first."
        messages = [
            SystemMessage(content="Create 5 comprehensive study flashcards based on the material. Use markdown **Q:** and **A:** format."),
            HumanMessage(content=f"Context:\n{context}")
        ]
        return self.llm.generate(messages).content
        
    def generate_quiz(self, subject_id: int) -> str:
        context = self._get_subject_context(subject_id)
        if not context: return "Please upload documents first."
        messages = [
            SystemMessage(content="Create a 3-question multiple choice quiz based on the material. Provide answers at the bottom."),
            HumanMessage(content=f"Context:\n{context}")
        ]
        return self.llm.generate(messages).content
        
    def record_quiz_score(self, subject_id: int, score: float, feedback: str):
        weak_topics = self.analytics.extract_weak_topics(feedback)
        qr = QuizResult(subject_id=subject_id, score=score, weak_topics=json.dumps(weak_topics))
        self.db.add(qr)
        self.db.commit()
        
    def get_subject_analytics(self, subject_id: int):
        quizzes = self.db.query(QuizResult).filter(QuizResult.subject_id == subject_id).all()
        return self.analytics.get_subject_insights(quizzes)
