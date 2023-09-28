from sqlalchemy.orm import Session

from orders import models


def get_cart(db: Session, user_id: int):
    if (
        cart := db.query(models.Cart)
        .filter(models.Cart.customer_id == user_id)
        .first()
    ):
        return cart


def add_cart(db: Session, user_id: int):
    cart = models.Cart(customer_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def update_cart_item_service(db: Session, cart_item_id: int, action: str, current_user_id: int):
    user_cart = get_cart(db=db, user_id=current_user_id)
    user_cart.update_cart_item(db=db, cart_item_id=cart_item_id, action='add')
    return user_cart
