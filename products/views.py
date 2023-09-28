from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database import get_db
from products import schemas
from products.services import (create_author, read_authors, update_author_data, delete_author, update_book, create_book,
                               read_books, read_book, read_author)
from users.authentication import check_admin_user

bearer_token = Depends(check_admin_user)

# router = APIRouter(prefix='/books', tags=["books"], dependencies=[Depends(check_admin_user)])
router = APIRouter(prefix='/books', tags=["books"], dependencies=[bearer_token])


@router.post("/authors/", response_model=schemas.Author)
def add_author_view(author: schemas.AuthorBase, db: Session = Depends(get_db), authorization: str = bearer_token):
    db_author = create_author(author=author, db=db)
    return db_author


@router.get("/authors/", response_model=List[schemas.Author])
def list_authors_view(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = read_authors(skip=skip, limit=limit, db=db)
    return authors


@router.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_view(author_id: int, db: Session = Depends(get_db)):
    author = read_author(author_id=author_id, db=db)
    return author


@router.put("/authors/{author_id}", response_model=schemas.Author)
def update_author_view(author_id: int, author: schemas.AuthorBase, db: Session = Depends(get_db)):
    db_author = update_author_data(author_id=author_id, author=author, db=db)
    return db_author


@router.delete("/authors/{author_id}")
def delete_author_view(author_id: int, db: Session = Depends(get_db)):
    delete_author(author_id=author_id, db=db)
    return {"message": "Author deleted"}


# Book CRUD API
@router.post("/", response_model=schemas.Book)
def add_book_view(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = create_book(book=book, db=db)
    return jsonable_encoder(db_book)


@router.get("/", response_model=List[schemas.Book])
def list_books_view(page: int = 0, page_size: int = 100, db: Session = Depends(get_db)):
    books = read_books(skip=page * page_size, limit=page_size, db=db)
    return books


@router.get("/{book_id}", response_model=schemas.Book)
def get_book_view(book_id: int, db: Session = Depends(get_db)):
    book = read_book(book_id=book_id, db=db)
    print(book.author, "<<<<<")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book_view(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = update_book(book_id=book_id, book=book, db=db)
    return db_book
