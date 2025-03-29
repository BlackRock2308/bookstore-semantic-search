from app.services.embedding import generate_embedding
import duckdb
from contextlib import asynccontextmanager
import os

DB_PATH = os.path.abspath("bookstore.db")

INITIAL_BOOKS = [
    "The 40 rules of the religion of Love",
    "The Psychology of money",
    "How to win friends and influence people",
    "The Art of War",
    "The Power of Now",
    "The Alchemist",
    "The intelligent investor",
    "A so long leter",
    "La plus secrète mémoire des hommes",
    "The milionaire fastlane",
    "The 7 habits of highly effective people",
    "The 48 Laws of Power",
]

def initialize_database():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS book_id_seq START 1;
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id BIGINT DEFAULT nextval('book_id_seq') PRIMARY KEY,
            title VARCHAR NOT NULL UNIQUE,
            embedding FLOAT[384] NOT NULL
        )
    """)
    return conn

@asynccontextmanager
async def lifespan(app):
    """Application lifespan event to initialize the database and preload data."""
    conn = initialize_database()
    try:
        # Clear existing data safely
        conn.execute("DELETE FROM books")
        
        # Insert initial books
        for title in INITIAL_BOOKS:
            try:
                embedding = await generate_embedding(title)
                conn.execute("""
                    INSERT INTO books (title, embedding)
                    VALUES (?, ?)
                    ON CONFLICT (title) DO UPDATE 
                    SET embedding = excluded.embedding
                """, [title, embedding])
            except Exception as e:
                print(f"Skipping duplicate or error for '{title}': {e}")
        
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")

    yield  # Keep app running

    conn.close()  # Close DB connection when app shuts down

def get_db():
    return duckdb.connect(DB_PATH)