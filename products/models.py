from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship('Books', back_populates='author')

    def __repr__(self):
        return self.name


class Books(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Authors', back_populates='books')
    cart_item = relationship('CartItem', back_populates='books')
    order_item = relationship('OrderItem', back_populates='books')
    price = Column(Float)

    def __repr__(self):
        return self.title

