from pydantic import BaseModel
from typing import List, Dict

class Metadata(BaseModel):
    source: str
    author: str

class Document(BaseModel):
    document_id: str
    content: str
    metadata: Metadata

class RetrievalResult(BaseModel):
    query: str
    retrieved_documents: List[Document]
    retrieval_method: str

class OutputModel(BaseModel):
    retrieval_result: RetrievalResult
    response: str