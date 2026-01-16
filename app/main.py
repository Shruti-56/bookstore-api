from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Book

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/books")
def add_book(title: str, author: str, db: Session = Depends(get_db)):
    book = Book(title=title, author=author)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
