from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    #realtionships with Book model
    books: list["Book"] = Relationship(back_populates="owner")


class UserCreate(SQLModel):
    name: str
    email: str
    college: str


class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str


# avoid circualr import by importing Book model here
from models.book_model import Book  # noqa: I001
User.model_rebuild()
