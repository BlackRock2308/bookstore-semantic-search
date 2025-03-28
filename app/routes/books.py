from fastapi import APIRouter, Depends
import duckdb
import numpy as np
from app.models.schemas import Book, SearchResult
from app.services.embedding import generate_embedding
from app.database.setup import get_db
from fastapi import HTTPException

router = APIRouter()

def cosine_similarity(a: list, b: list) -> float:
    a_array = np.array(a)
    b_array = np.array(b)
    return np.dot(a_array, b_array) / (np.linalg.norm(a_array) * np.linalg.norm(b_array))

@router.post("/add-book/")
async def add_book(book: Book, conn=Depends(get_db)):
    try:
        embedding = generate_embedding(book.title)
        conn.execute("""
            INSERT INTO books (title, embedding)
            VALUES (?, ?)
            ON CONFLICT (title) DO UPDATE 
            SET embedding = excluded.embedding
        """, [book.title, embedding])
        conn.commit()
        return {"message": "Book added/updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/", response_model=list[SearchResult])
async def search_books(
    query: str, 
    limit: int = 2,
    conn=Depends(get_db)
):
    query_embedding = generate_embedding(query)
    result = conn.execute("SELECT title, embedding FROM books").fetchall()
    
    # Use a dictionary to track max similarity per title
    title_map = {}
    
    for title, db_embedding in result:
        similarity = cosine_similarity(query_embedding, db_embedding)
        # Keep only the highest similarity for each title
        if title not in title_map or similarity > title_map[title]:
            title_map[title] = similarity
    
    # Sort and limit results
    sorted_results = sorted(
        title_map.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:limit]
    
    return [{"title": title, "similarity": float(sim)} for title, sim in sorted_results]