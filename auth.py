from werkzeug.security import generate_password_hash, check_password_hash
from repository import get_user_by_username, create_user

def register_user(username, password):
    if get_user_by_username(username):
        return None  # User exists
    hashed_password = generate_password_hash(password)
    return create_user(username, hashed_password)

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user.hashed_password, password):
        return user
    return None
