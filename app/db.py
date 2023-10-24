import os
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.engine import Engine

connection_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("POSTGRES_DB")}'


def create_db_and_tables() -> Engine:
    print("Creating models.")
    # Import models so that they are registered for SQLModel.metadata
    import models
    engine = create_engine(connection_string, echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    print("Created models.")
    return engine