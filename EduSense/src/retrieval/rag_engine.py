"""
rag_engine.py - Retrieval-Augmented Generation for AI Tutoring.
"""

import json
from typing import List, Dict, Any, Tuple
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document
from src.ai.llm_manager import LLMManager
from src.storage.faiss_manager import FaissManager
import logging

logger = logging.getLogger(__name__)

TUTOR_PROMPT = """You are EduSense, an expert AI Tutor. 
Your goal is to help the student understand the material based ONLY on the provided context.
If you don't know the answer based on the context, politely guide them to check other sources.
Do not hallucinate facts. Be encouraging, educational, and clear."""

class RAGEngine:
    def __init__(self, llm_manager: LLMManager, faiss_manager: FaissManager):
        self.llm = llm_manager
        self.faiss = faiss_manager
        
    def retrieve(self, subject_id: int, query: str, k: int = 5) -> List[Document]:
        vectorstore = self.faiss.load_vectorstore(subject_id)
        if not vectorstore:
            return []
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(query)
        
    def build_context(self, docs: List[Document]) -> Tuple[str, List[Dict]]:
        context_parts = []
        citations = []
        for idx, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Unknown Document')
            text = doc.page_content.strip()
            context_parts.append(f"--- Document [{idx+1}]: {source} ---\n{text}\n")
            citations.append({
                "id": idx + 1,
                "source": source,
                "snippet": text[:100] + "..."
            })
        return "\n".join(context_parts), citations

    def tutor_ask(self, subject_id: int, query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        docs = self.retrieve(subject_id, query)
        context_str, citations = self.build_context(docs)
        
        prompt = f"Study Material Context:\n{context_str}\n\nStudent Question: {query}"
        messages = [SystemMessage(content=TUTOR_PROMPT)]
        
        if history:
            from langchain_core.messages import AIMessage
            for msg in history:
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(AIMessage(content=msg['content']))
                    
        messages.append(HumanMessage(content=prompt))
        
        try:
            response = self.llm.generate(messages)
            return {
                "answer": response.content,
                "citations": citations
            }
        except Exception as e:
            logger.error(f"Tutor RAG error: {e}")
            return {"answer": "I'm having trouble thinking right now. Please try again.", "citations": []}
