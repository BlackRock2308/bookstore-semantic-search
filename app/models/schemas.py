from pydantic import BaseModel

class Book(BaseModel):
    title: str

class SearchResult(BaseModel):
    title: str
    similarity: float