"""
planning_service.py - Study Planners.
"""

from sqlalchemy.orm import Session
from src.storage.database import StudyPlan
from src.ai.llm_manager import LLMManager
from src.storage.faiss_manager import FaissManager
from langchain_core.messages import SystemMessage, HumanMessage

class PlanningService:
    def __init__(self, db: Session, llm: LLMManager, faiss: FaissManager):
        self.db = db
        self.llm = llm
        self.faiss = faiss
        
    def generate_plan(self, subject_id: int, plan_type: str, time_available: str) -> str:
        vectorstore = self.faiss.load_vectorstore(subject_id)
        context = ""
        if vectorstore:
            docs = vectorstore.as_retriever(search_kwargs={"k": 10}).invoke("syllabus chapters core topics")
            context = "\n".join([d.page_content for d in docs])
            
        system = f"You are a study planner. Create a highly structured {plan_type} study plan for the student. They have {time_available} available."
        messages = [
            SystemMessage(content=system),
            HumanMessage(content=f"Subject Material Context:\n{context}")
        ]
        
        plan_content = self.llm.generate(messages).content
        
        # Save to DB
        plan = StudyPlan(subject_id=subject_id, plan_type=plan_type, content=plan_content)
        self.db.add(plan)
        self.db.commit()
        
        return plan_content
