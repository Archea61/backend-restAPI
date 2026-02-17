from sqlalchemy.orm import Session
from .models import User, Product, Order, OrderItem
from .auth import hash_password


def create_user(db: Session, email: str, name: str, password: str):
    user = User(
        email=email,
        name=name,
        password=hash_password(password),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_product(db: Session, name: str, price: float):
    product = Product(name=name, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_order(db: Session, user_id: int, items: list):
    order = Order(user_id=user_id, total_price=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    total_price = 0

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity
            )
            db.add(order_item)
            total_price += product.price * item.quantity

    order.total_price = total_price
    db.commit()
    db.refresh(order)
    return order