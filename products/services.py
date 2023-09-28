from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from products import schemas, models


def create_author(author: schemas.AuthorBase, db: Session):
    if author := models.Authors.filter(
            models.Authors.name == author.name
    ).first():
        raise HTTPException(status_code=400, detail="Author already exists")
    db_author = models.Authors(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = db.query(models.Authors).offset(skip).limit(limit).all()
    return authors


def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Authors).filter(models.Authors.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def update_author_data(author_id: int, author: schemas.AuthorBase, db: Session = Depends(get_db)):
    db_author = db.query(models.Authors).filter(models.Authors.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    for field, value in vars(author).items():
        if value is not None:
            setattr(db_author, field, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(models.Authors).filter(models.Authors.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted"}


def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Books(title=book.title, author_id=book.author_id, price=book.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Books).offset(skip).limit(limit).all()
    return books


def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Books).filter(models.Books.book_id == book_id).first()
    db_book.update(id=book_id, data=book)
    db.commit()
    db.refresh(db_book)
    return db_book
