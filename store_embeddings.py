from sentence_transformers import SentenceTransformer
import psycopg2
import json
from config import db_config
from knowledge_base import documents

def store_embeddings():
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    try:
        # Connect to database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
        """)

        # Clear existing data
        cursor.execute("TRUNCATE TABLE knowledge_base")

        # Process each document
        for doc in documents:
            # Generate embedding for the document content
            embedding = model.encode(doc['content'])
            
            # Insert document and its embedding
            cursor.execute("""
                INSERT INTO knowledge_base (title, content, embedding) 
                VALUES (%s, %s, %s)
            """, (doc['title'], doc['content'], json.dumps(embedding.tolist())))

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

if __name__ == "__main__":
    store_embeddings()