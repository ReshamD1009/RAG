from sentence_transformers import SentenceTransformer
import psycopg2
from config import db_config
from knowledge_base import documents

def store_embeddings():
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    try:
        # Connect to database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Enable pgvector extension if not already enabled
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Create table with vector type if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector(384)  -- dimension size for all-MiniLM-L6-v2
            )
        """)
        
        # Create an index for faster similarity search
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS embedding_idx 
            ON knowledge_base 
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """)

        # Clear existing data
        cursor.execute("TRUNCATE TABLE knowledge_base")

        # Process each document
        for doc in documents:
            # Generate embedding for the document content
            embedding = model.encode(doc['content'])
            
            # Insert document and its embedding directly as vector type
            cursor.execute("""
                INSERT INTO knowledge_base (title, content, embedding) 
                VALUES (%s, %s, %s)
            """, (doc['title'], doc['content'], embedding.tolist()))

        connection.commit()
        print(f"Successfully stored {len(documents)} documents in the database.")

    except Exception as e:
        print(f"Error storing embeddings: {e}")
        if 'connection' in locals():
            connection.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

store_embeddings()