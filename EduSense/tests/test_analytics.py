import pytest
from src.analytics.analytics_engine import AnalyticsEngine
from src.storage.database import QuizResult

class MockLLM:
    def generate(self, messages):
        class Response:
            content = '["photosynthesis", "cellular respiration"]'
        return Response()

def test_analytics_extraction():
    engine = AnalyticsEngine(MockLLM())
    topics = engine.extract_weak_topics("I struggled with photosynthesis and cellular respiration.")
    
    assert isinstance(topics, list)
    assert len(topics) == 2
    assert topics[0] == "photosynthesis"

def test_subject_insights():
    engine = AnalyticsEngine(MockLLM())
    quizzes = [
        QuizResult(score=80.0, weak_topics='["photosynthesis"]'),
        QuizResult(score=90.0, weak_topics='["mitosis", "photosynthesis"]')
    ]
    
    insights = engine.get_subject_insights(quizzes)
    assert insights['average_score'] == 85.0
    assert insights['quizzes_taken'] == 2
    assert "photosynthesis" in insights['weak_areas']
