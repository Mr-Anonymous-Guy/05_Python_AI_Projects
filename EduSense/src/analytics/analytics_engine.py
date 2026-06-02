"""
analytics_engine.py - Tracks learning progress and identifies weak topics.
"""

from typing import List, Dict, Any
import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.ai.llm_manager import LLMManager
from src.storage.database import QuizResult

class AnalyticsEngine:
    def __init__(self, llm_manager: LLMManager):
        self.llm = llm_manager

    def extract_weak_topics(self, quiz_feedback: str) -> List[str]:
        """Uses LLM to extract an array of weak topics from quiz feedback text."""
        system = "You are an analytics parser. Extract a list of weak topics the student struggled with from the feedback. Return ONLY a valid JSON array of strings. Do not include markdown code blocks or any other text."
        messages = [
            SystemMessage(content=system),
            HumanMessage(content=f"Feedback: {quiz_feedback}")
        ]
        try:
            response = self.llm.generate(messages).content
            topics = json.loads(response.strip())
            return topics if isinstance(topics, list) else []
        except Exception:
            return []

    def get_subject_insights(self, quizzes: List[QuizResult]) -> Dict[str, Any]:
        """Aggregates analytics for a subject."""
        if not quizzes:
            return {"average_score": 0.0, "quizzes_taken": 0, "weak_areas": []}
            
        avg = sum(q.score for q in quizzes) / len(quizzes)
        
        all_weak_topics = []
        for q in quizzes:
            if q.weak_topics:
                try:
                    topics = json.loads(q.weak_topics)
                    all_weak_topics.extend(topics)
                except Exception:
                    pass
                    
        # Simple frequency count
        from collections import Counter
        freq = Counter(all_weak_topics)
        top_weak = [topic for topic, count in freq.most_common(5)]
        
        return {
            "average_score": round(avg, 2),
            "quizzes_taken": len(quizzes),
            "weak_areas": top_weak
        }
