from sqlmodel import Field, Relationship, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float
    is_sold: bool = Field(default=False)

    # relationship with User model
    user_id: int = Field(foreign_key="user.id")
    owner: "User" = Relationship(back_populates="books")


class BookCreate(SQLModel):
    title: str
    author: str
    price: float
    user_id: int


class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: float
    is_sold: bool
    user_id: int


from models.user_model import User

Book.model_rebuild()
