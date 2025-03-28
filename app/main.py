from fastapi import FastAPI
from dotenv import load_dotenv
from app.database.setup import lifespan
from app.routes.books import router as books_router
from app.database.setup import get_db
import os

load_dotenv()

app = FastAPI(lifespan=lifespan)
app.include_router(books_router, prefix="/api/books")

# Add initial books at startup
INITIAL_BOOKS = [
    "The Great Gatsby",
    "To Kill a Mockingbird",
    "1984",
    "Pride and Prejudice",
    "The Catcher in the Rye",
    "Moby Dick",
    "War and Peace",
    "The Odyssey"
]

@app.on_event("startup")
async def startup_event():
    conn = get_db()
    try:
        # Clear existing data using TRUNCATE to reset sequences
        conn.execute("TRUNCATE TABLE books")
        
        # Insert initial books with conflict handling
        for title in INITIAL_BOOKS:
            try:
                embedding = generate_embedding(title)
                conn.execute("""
                    INSERT INTO books (title, embedding)
                    VALUES (?, ?)
                    ON CONFLICT (title) DO UPDATE 
                    SET embedding = excluded.embedding
                """, [title, embedding])
            except Exception as e:
                print(f"Skipping duplicate: {title}")
        
        conn.commit()
    finally:
        conn.close()