from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class ShowBook(BaseModel):
    book_id: int
    title: str
    price: float

    class Config:
        orm_mode = True


class Author(AuthorBase):
    books: List[ShowBook] = []

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author_id: int
    price: float


class Book(BaseModel):
    title: str
    book_id: int
    author_id: int
    price: float
    author: Author

    class Config:
        orm_mode = True
