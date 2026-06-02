"""
faiss_manager.py - Manage FAISS vector store operations for Subjects.
"""

import os
import shutil
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document as LC_Document
from src.config import FAISS_INDEX_PATH
import logging

logger = logging.getLogger(__name__)

class FaissManager:
    """Manages the FAISS vector database for subjects."""
    
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        
    def _get_subject_path(self, subject_id: int) -> str:
        """Returns the FAISS path for a specific subject."""
        return os.path.join(FAISS_INDEX_PATH, f"subject_{subject_id}")

    def load_vectorstore(self, subject_id: int) -> Optional[FAISS]:
        """Loads a FAISS index from disk for a specific subject."""
        path = self._get_subject_path(subject_id)
        if os.path.exists(path):
            try:
                return FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                logger.error(f"Failed to load FAISS index at {path}: {e}")
                return None
        return None

    def add_documents(self, subject_id: int, documents: List[LC_Document]) -> int:
        """Adds embedded documents to a subject's FAISS index."""
        path = self._get_subject_path(subject_id)
        
        vectorstore = self.load_vectorstore(subject_id)
        if vectorstore is None:
            vectorstore = FAISS.from_documents(documents, self.embeddings)
        else:
            vectorstore.add_documents(documents)
            
        vectorstore.save_local(path)
        logger.info(f"Saved {len(documents)} chunks to FAISS at {path}")
        return len(documents)

    def delete_subject(self, subject_id: int) -> bool:
        """Deletes the FAISS index for a subject."""
        path = self._get_subject_path(subject_id)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                return True
            except Exception as e:
                logger.error(f"Failed to delete FAISS index at {path}: {e}")
                return False
        return True
