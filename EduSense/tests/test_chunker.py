import pytest
from src.document.chunker import DocumentChunker
from langchain_core.documents import Document

def test_document_chunker():
    chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
    docs = [Document(page_content="This is a very long sentence that needs to be chunked properly by the DocumentChunker system for EduSense.", metadata={"source": "test.txt"})]
    
    chunks = chunker.chunk_documents(docs)
    
    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "test.txt"
    assert len(chunks[0].page_content) <= 50
