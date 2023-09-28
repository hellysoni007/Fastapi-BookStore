from typing import List

from pydantic import BaseModel

from products.schemas import ShowBook


class CartItem(BaseModel):
    book_id: int
    quantity: int
    books: ShowBook

    class Config:
        orm_mode = True


class Cart(BaseModel):
    customer_id: int
    items: List[CartItem] = []

    class Config:
        orm_mode = True
