from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    # tags: list[Tag]
    timestamp: datetime
