from db import SessionLocal
from models import User, Product, Order

def get_user_by_username(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def get_user_by_id(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

def create_user(username, hashed_password):
    db = SessionLocal()
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_product(product_id):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    return product

def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

def create_order(user_id, product_id, quantity):
    db = SessionLocal()
    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    db.close()
    return order

def reduce_product_stock(product_id, quantity):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product and product.stock >= quantity:
        product.stock -= quantity
        db.commit()
        db.close()
        return True
    db.close()
    return False
