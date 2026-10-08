from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///bookExchange.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
