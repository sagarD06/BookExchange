from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.user_model import User, UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def get_all_users(session: Annotated[Session, Depends(get_session)]):
    """Retrieve all users from the database."""
    users = session.exec(select(User)).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, session: Annotated[Session, Depends(get_session)]):
    """Retrieve a user by their ID."""
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Create a new user in the database."""
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
