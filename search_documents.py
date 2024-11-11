from sentence_transformers import SentenceTransformer
from typing import List, Dict
from config import db_config
import psycopg2
import numpy as np

# Initialize Sentence-Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_documents(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    try:
        # Generate embedding for the query
        query_embedding = model.encode(query).tolist()  # Convert to list
        
        # Connect to PostgreSQL
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        # Using pgvector's <-> operator for cosine distance search
        cursor.execute("""
            SELECT title, content
            FROM knowledge_base
            ORDER BY embedding <-> %s::vector
            LIMIT %s
        """, (query_embedding, top_k))
        
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return [{"title": title, "content": content} for title, content in results]
        
    except Exception as e:
        print(f"Error while searching documents: {e}")
        return []
