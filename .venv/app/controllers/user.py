from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User ,db

## Authentication
def create_user(first_name, last_name, email, password, address,dob,gender,is_admin=False):
    hashed_password = generate_password_hash(password)
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        address=address,
        dob=dob,
        password=hashed_password,
        is_admin=is_admin
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def get_all_users(include_admin):
    user = None
    if include_admin:
        user = User.query.filter_by(is_admin=True)
    else:
        user = User.query.filter_by(is_admin=False)
    return user
def get_user_by_id(user_id):
    return User.query.get(user_id)