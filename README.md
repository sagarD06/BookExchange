# Book Exchange API

A FastAPI-based book exchange application that lets users register and manage books for sale. The project stores data in SQLite and exposes REST API endpoints for user and book management.

## Features

- User registration and lookup
- Book creation, listing, updates, and deletion
- Filter books by title, author, and price range
- Mark books as sold
- API key protection on book mutation routes
- Swagger UI for interactive API testing

## Tech Stack

- Python 3
- FastAPI
- SQLModel
- SQLite
- Uvicorn

## Project Structure

```text
book_exchange/
├── auth.py
├── database.py
├── main.py
├── requirements.txt
├── bookExchange.db
├── models/
│   ├── __init__.py
│   ├── book_model.py
│   └── user_model.py
├── routes/
│   ├── __init__.py
│   ├── book_routes.py
│   └── user_routes.py
└── README.md
```

## Requirements

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

From the project root:

```bash
uvicorn main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

Swagger docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Database

This project uses SQLite with the database file:

```text
bookExchange.db
```

Tables are created automatically when the app starts via the lifespan hook in `main.py`.

## Authentication

Book mutation endpoints require an API key header:

```http
X-API-Key: MySecretAPIKey
```

The key is defined in `auth.py` and should be treated as a demo secret for local development.

## API Endpoints

### Health Check

- `GET /` — check if the API is running

### Users

- `GET /users/` — list all users
- `GET /users/{user_id}` — fetch a user by ID
- `POST /users/` — register a user

### Books

- `GET /books/` — list available books
- `POST /books/` — create a book
- `PATCH /books/{book_id}` — update a book
- `PATCH /books/{book_id}/mark_sold` — mark a book as sold
- `DELETE /books/{book_id}` — delete a book

## Example Requests

### Register a user

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "college": "ABC University"
  }'
```

### Create a book

```bash
curl -X POST "http://127.0.0.1:8000/books/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: MySecretAPIKey" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "price": 25.5,
    "user_id": 1
  }'
```

### List books

```bash
curl "http://127.0.0.1:8000/books/"
```

## Notes

- This project is a simple API prototype and is best suited for local development or educational use.
- For production use, consider moving the API key to environment variables, adding validation, improving error handling, and using a proper database such as PostgreSQL.
