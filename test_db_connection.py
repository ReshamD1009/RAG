import psycopg2
from config import db_config

def test_db_connection():
    try:
        # Attempt to connect to the database
        conn = psycopg2.connect(**db_config)
        print("Successfully connected to the database!")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL database version: {db_version[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_db_connection()