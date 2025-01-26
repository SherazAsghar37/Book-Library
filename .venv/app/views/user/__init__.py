from flask import Blueprint

user_bp = Blueprint("user", __name__)

from app.views.user import user