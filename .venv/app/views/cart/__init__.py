from flask import Blueprint

cart_bp = Blueprint("cart", __name__)

from app.views.cart import cart