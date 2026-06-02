"""
subject_service.py - Orchestrates Subject and Document logic.
"""

import os
from sqlalchemy.orm import Session
from src.storage.database import Subject, Document as DBDocument
from src.storage.faiss_manager import FaissManager
from src.document.loader import DocumentLoader
from src.document.chunker import DocumentChunker
from src.config import DATA_DIR
import logging

logger = logging.getLogger(__name__)

class SubjectService:
    def __init__(self, db: Session, faiss_manager: FaissManager):
        self.db = db
        self.faiss = faiss_manager
        self.chunker = DocumentChunker()
        
    def create_subject(self, name: str, description: str = "") -> Subject:
        subject = Subject(name=name, description=description)
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject
        
    def get_subjects(self):
        return self.db.query(Subject).all()
        
    def get_subject(self, subject_id: int):
        return self.db.query(Subject).filter(Subject.id == subject_id).first()
        
    def add_document(self, subject_id: int, file_bytes: bytes, filename: str) -> bool:
        subject_dir = os.path.join(DATA_DIR, f"subject_{subject_id}")
        os.makedirs(subject_dir, exist_ok=True)
        filepath = os.path.join(subject_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(file_bytes)
            
        try:
            docs = DocumentLoader.load_file(filepath, filename)
            chunks = self.chunker.chunk_documents(docs)
            if not chunks:
                return False
            self.faiss.add_documents(subject_id, chunks)
            
            db_doc = DBDocument(subject_id=subject_id, filename=filename, filepath=filepath, num_chunks=len(chunks))
            self.db.add(db_doc)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Doc error: {e}")
            return False
