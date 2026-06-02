"""
loader.py - Document loaders for academic and study materials.
"""

import os
import tempfile
import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader
)

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles parsing of PDF, DOCX, and TXT educational files."""
    
    @staticmethod
    def load_file(file_path: str, filename: str = None) -> List[Document]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        if not filename:
            filename = os.path.basename(file_path)
            
        documents = []
        try:
            if ext == '.pdf':
                loader = PyMuPDFLoader(file_path)
                documents = loader.load()
            elif ext == '.docx':
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
            elif ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
                
            for doc in documents:
                doc.metadata['source'] = filename
                
            return documents
        except Exception as e:
            logger.error(f"Error loading document {filename}: {e}")
            raise e

    @staticmethod
    def load_bytes(file_bytes: bytes, filename: str) -> List[Document]:
        ext = os.path.splitext(filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name
            
        try:
            return DocumentLoader.load_file(temp_path, filename)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
