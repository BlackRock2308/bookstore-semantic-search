from fastapi import FastAPI
from app.database.setup import lifespan
from app.routes.books import router as books_router



app = FastAPI(lifespan=lifespan)
app.include_router(books_router, prefix="/api/books")

