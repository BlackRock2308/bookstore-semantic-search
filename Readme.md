# Bookstore Semantic Search API

This project is a FastAPI-based application for managing a bookstore and performing semantic search on book titles using embeddings and cosine similarity.

## Features

- **Add Books**: Add new books to the database or update their embeddings if they already exist.
- **Search Books**: Perform semantic searches on book titles using a query string and retrieve the most relevant results.

## Project Structure

```
.env
.gitignore
bookstore.db
initial_books.txt
requirements.txt
app/
    main.py
    database/
        setup.py
    models/
        schemas.py
    routes/
        books.py
    services/
        embedding.py
myenv/
```

### Key Components

- **Routes**: 
  - [`books.py`](app/routes/books.py): Contains endpoints for adding books and searching books.
- **Models**:
  - [`schemas.py`](app/models/schemas.py): Defines the data models for the API.
- **Services**:
  - [`embedding.py`](app/services/embedding.py): Handles the generation of embeddings for book titles.
- **Database**:
  - [`setup.py`](app/database/setup.py): Manages the database connection.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd bookstore-semantic-search
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Ensure `bookstore.db` is initialized with a `books` table:
     ```sql
     CREATE TABLE books (
         title TEXT PRIMARY KEY,
         embedding BLOB
     );
     ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Example Endpoints

#### Add a Book
- **Endpoint**: `POST /api/books/add-book/`
- **Request Body**:
  ```json
  {
    "title": "The Lord of the Rings"
  }
  ```

#### Search Books
- **Endpoint**: `GET /api/books/search/`
- **Query Parameters**:
  - `query`: The search string (e.g., "classic novel").
  - `limit`: Number of results to return (default: 2).

## Testing

You can test the API using tools like `curl`, Postman, or directly through the Swagger UI.

## License

This project is licensed under the MIT License.