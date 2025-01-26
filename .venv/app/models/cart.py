from .. import db
from datetime import datetime


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user = db.relationship('User', backref='cart')

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    cart = db.relationship('Cart', backref='items')
    book = db.relationship('Book')

    def __repr__(self):
        return f"<CartItem {self.book.title} >"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(50), nullable=False, default='Pending')  # e.g., Pending, Completed, Canceled
    address = db.Column(db.String(255), nullable=False)  # Shipping address
    phone_number = db.Column(db.String(20), nullable=False)  # Contact phone number

    user = db.relationship('User', backref='orders')  # Relationship to User

    def __repr__(self):
        return f"<Order {self.id} by User {self.user_id}>"
    
class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    order = db.relationship('Order', backref='order_details')  # Relationship to Order
    book = db.relationship('Book')  # Relationship to Book

    def __repr__(self):
        return f"<OrderDetail Order {self.order_id} - Book {self.book_id}>"