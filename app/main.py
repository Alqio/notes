from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

import db
from models import Note, Tag, NoteBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = db.create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)
engine = None



@app.get("/")
def read_root():
    return {"version": "0.0.1"}


@app.post("/notes/", response_model=Note)
def create_note(note: NoteBase):
    print("in create note", note)
    tag_names = [tag for tag in note.tags]
    print(tag_names)

    with Session(engine) as session:
        # Create tag objects for tags that do not exist yet
        note = Note.from_orm(note)

        for name in tag_names:
            tag = session.exec(select(Tag).where(Tag.name == name)).first()
            if tag is None:
                tag = Tag(name=name, notes=[note])
                session.add(tag)
            else:
                tag.notes.append(note)

        session.add(note)
        session.commit()
        session.refresh(note)
        return note


@app.post("/tags/")
def create_tag(tag: Tag) -> Tag:
    print(tag)
    with Session(engine) as session:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


@app.get("/notes/", response_model=list[NoteBase])
def get_notes():
    with Session(engine) as session:
        notes = session.exec(select(Note)).all()

        base_notes: list[NoteBase] = []
        for note in notes:
            n = NoteBase(text=note.text, updated_at=note.updated_at, tags=[tag.name for tag in note.tags])

            base_notes.append(n)
            
        return base_notes


@app.get("/tags/")
def get_tags() -> list[Tag]:
    with Session(engine) as session:
        tags = session.exec(select(Tag)).all()
        return tags



@app.get("/notes/{note_id}")
def read_item(note_id: int):
    with Session(engine) as session:
        try:
            note = session.exec(select(Note).where(Note.id == note_id)).one()
            return note
        except:
            raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found.")
