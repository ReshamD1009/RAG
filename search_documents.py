from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
import json
import numpy as np
from typing import List, Dict
from config import db_config

# Initialize Sentence-Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_documents(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    try:
        # Generate embedding for the query
        query_embedding = model.encode(query)

        # Connect to PostgreSQL
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Retrieve all documents with embeddings
        cursor.execute("SELECT id, title, content, embedding FROM knowledge_base")
        documents = cursor.fetchall()

        # Calculate similarities
        similarities = []
        for doc_id, title, content, embedding_str in documents:
            embedding = np.array(json.loads(embedding_str))
            similarity = cosine_similarity([query_embedding], [embedding])[0][0]
            similarities.append((similarity, title, content))

        # Sort by similarity and get top_k
        top_results = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]

        cursor.close()
        connection.close()

        return [{"title": title, "content": content} for _, title, content in top_results]

    except Exception as e:
        print(f"Error while searching documents: {e}")
        return []