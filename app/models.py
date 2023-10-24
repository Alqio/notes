from typing import Optional
from datetime import datetime
from typing import List
from pydantic import BaseModel

from sqlmodel import SQLModel, Field, Relationship


class NoteTagLink(SQLModel, table=True):
    tag_name: Optional[str] = Field(default=None, foreign_key="tag.name", primary_key=True)
    note_id: Optional[int] = Field(default=None, foreign_key="note.id", primary_key=True)


class Tag(SQLModel, table=True):
    name: str = Field(default="tag", primary_key=True, unique=True)

    notes: List["Note"] = Relationship(back_populates="tags", link_model=NoteTagLink)


class NoteBase(BaseModel):
    text: str
    tags: List[str]
    updated_at: Optional[datetime]


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
 
    tags: List[Tag] = Relationship(back_populates="notes", link_model=NoteTagLink)

