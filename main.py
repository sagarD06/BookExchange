from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routes.book_routes import router as book_router
from routes.user_routes import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created successfully.`")

    # cleanup code can be added here if needed
    yield
    print("Application shutdown complete.")


app = FastAPI(
    title="Book Exchange App API's",
    description="FastAPI application for Book Exchange App",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(book_router)


@app.get("/")
def health_check():
    return {"message": "Book Exchange App API's is running!"}
