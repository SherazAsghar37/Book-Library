from flask import Blueprint, Flask, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from datetime import datetime
from flask_wtf import CSRFProtect

# from app.controllers.user import create_user

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    csrf = CSRFProtect(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    @app.route('/some_route')
    def some_route():
        if 'logged_in' in session:
            pass
        else:
            return redirect(url_for('user.login'))

    
    # Register blueprints
    from .views.home import main
    from .views.books import books_bp as books
    from .views.user import user_bp as user
    from .views.cart import cart_bp as cart
    app.register_blueprint(main)
    app.register_blueprint(books)
    app.register_blueprint(user)
    app.register_blueprint(cart)
    
 
    
    with app.app_context():
        db.create_all()
        from app.models.user import User
        print(f"Checking for existing user with")
        admin_email = 'admin@gmail.com'
        existing_user = User.query.filter_by(email=admin_email).first()
        from app.controllers.user import create_user
        dob_date = datetime.strptime("2003-1-1", '%Y-%m-%d').date()
        if existing_user is None:
            create_user(
                first_name='Admin',
                last_name='Admin',
                email=admin_email,
                password='Admin',
                address='Admin Address',
                dob=dob_date,
                gender="Male",
                is_admin=True
            )
            print("Admin user created.")
        else:
            print("Admin user already exists.")
    return app