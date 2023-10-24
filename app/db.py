import os
from sqlmodel import create_engine, SQLModel
from sqlalchemy.engine import URL

connection_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("POSTGRES_DB")}'
print(connection_string)

engine = create_engine(f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("POSTGRES_DB")}', echo=True)

SQLModel.metadata.create_all(engine)
