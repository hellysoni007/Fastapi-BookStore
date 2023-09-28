from sqlalchemy import Column, Integer, ForeignKey, DATE
from sqlalchemy.orm import relationship, Session

from database import Base
from orders import schemas


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.book_id'))
    qty = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.id'))
    orders = relationship('Orders', back_populates='items')
    books = relationship('Books', back_populates='order_item')


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    items = relationship('OrderItem', back_populates='orders')
    order_date = DATE


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    quantity = Column(Integer)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    cart = relationship("Cart", back_populates="items")
    books = relationship("Books", back_populates="cart_item")


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    items = relationship("CartItem", back_populates="cart")

    def add_cart_item(self, data: schemas.CartItem, db: Session):
        cart_item = CartItem(**data.__dict__, cart_id=self.id)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

    def update_cart_item(self, db: Session, cart_item_id: int, action: str):
        if cart_item := db.query(CartItem).filter(CartItem.id == cart_item_id).first():
            if action == 'add':
                cart_item.quantity += 1
            elif action == 'remove':
                db.delete(cart_item)
            elif action == 'subtract':
                if cart_item.quantity > 0:
                    cart_item.quantity -= 1
                else:
                    db.delete(cart_item)
            db.commit()
            db.refresh(self)
            return self.items
