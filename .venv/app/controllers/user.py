from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, db

class UserController:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def create_user(self, first_name, last_name, email, password, address, dob, gender, is_admin=False):
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

    def login_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    def get_all_users(self, include_admin=False):
        if include_admin:
            users = User.query.filter_by(is_admin=True).all()
        else:
            users = User.query.filter_by(is_admin=False).all()
        return users

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
