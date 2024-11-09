import psycopg2
from config import db_config
from store_embeddings import store_embeddings

def init_database():
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            dbname='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_config['dbname']}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_config['dbname']}")
            print(f"Database {db_config['dbname']} created successfully!")
        
        cursor.close()
        conn.close()

        # Store embeddings
        store_embeddings()
        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error during database initialization: {e}")

if __name__ == "__main__":
    init_database()