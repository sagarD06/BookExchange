from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables


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


@app.get("/")
def health_check():
    return {"message": "Book Exchange App API's is running!"}
