from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from database import get_db
from orders import schemas, services
from users.authentication import get_current_user
from users.schemas import User

cart_router = APIRouter(prefix='/cart', tags=["cart"], dependencies=[Depends(get_current_user)])
order_router = APIRouter(prefix='/order', tags=["order"], dependencies=[Depends(get_current_user)])


@cart_router.post('/add/')
def add_to_cart_view(request: schemas.CartItem, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if not (user_cart := services.get_cart(db=db, user_id=current_user.id)):
        user_cart = services.add_cart(db=db, user_id=current_user.id)
    cart_items = user_cart.add_cart_item(request, db=db)
    return {'cart_items': cart_items}


@cart_router.put('/{cart_item_id}/plus/', response_model=schemas.Cart)
def add_qty_by_one_to_cart(cart_item_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return services.update_cart_item_service(db=db, cart_item_id=cart_item_id, action='add',
                                             current_user_id=current_user.id)


@cart_router.put('/{cart_item_id}/minus/')
def decrease_by_one_from_cart(cart_item_id: int, db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    return services.update_cart_item_service(db=db, cart_item_id=cart_item_id, action='subtract',
                                             current_user_id=current_user.id)


@cart_router.put('/{cart_item_id}/remove/')
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return services.update_cart_item_service(db=db, cart_item_id=cart_item_id, action='remove',
                                             current_user_id=current_user.id)


@cart_router.get('/', response_model=schemas.Cart)
def show_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_cart = services.get_cart(db=db, user_id=current_user.id)
    return user_cart

@order_router.post('/place-order/')
def place_order_view(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_cart = services.get_cart(db=db, user_id=current_user.id)
    order = services.place_order(db=db,user_id=current_user.id)
    return user_cart