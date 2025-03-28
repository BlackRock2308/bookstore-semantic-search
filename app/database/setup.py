import duckdb
from contextlib import asynccontextmanager
import os

def initialize_database():
    db_path = os.path.abspath("bookstore.db")
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id BIGINT PRIMARY KEY,
            title VARCHAR NOT NULL UNIQUE,
            embedding FLOAT[384] NOT NULL
        )
    """)
    conn.execute("CREATE SEQUENCE IF NOT EXISTS book_id_seq START 1;")
    conn.execute("""
        ALTER TABLE books ALTER COLUMN book_id 
        SET DEFAULT nextval('book_id_seq')
    """)
    return conn

@asynccontextmanager
async def lifespan(app):
    conn = initialize_database()
    yield
    conn.close()

def get_db():
    return initialize_database()