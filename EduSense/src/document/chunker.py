"""
chunker.py - Smart chunking for educational materials.
"""

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentChunker:
    """Handles splitting educational documents into optimal context windows."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or CHUNK_OVERLAP
        # Prioritize natural breaks like paragraphs for studying
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        return self.splitter.split_documents(documents)
