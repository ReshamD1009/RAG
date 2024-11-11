from pydantic import BaseModel, Field
from typing import List

class Metadata(BaseModel):
    source: str = Field(
        description="The source or origin of the document"
    )
    author: str = Field(
        description="The author of the document"
    )

class Document(BaseModel):
    document_id: str = Field(
        description="Unique identifier for the document"
    )
    content: str = Field(
        description="The main content/text of the document"
    )
    metadata: Metadata = Field(
        description="Associated metadata for the document"
    )

class RetrievalResult(BaseModel):
    query: str = Field(
        description="The search query used for retrieval"
    )
    retrieved_documents: List[Document] = Field(
        description="List of documents retrieved from the search"
    )
    retrieval_method: str = Field(
        description="The method used for document retrieval"
    )

class OutputModel(BaseModel):
    retrieval_result: RetrievalResult = Field(
        description="The results from the document retrieval process"
    )
    response: str = Field(
        description="The generated response based on the retrieved documents"
    )
