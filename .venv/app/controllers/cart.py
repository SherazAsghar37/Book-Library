import datetime
from app.models.cart import Cart, CartItem, db, Order, OrderDetail

class CartController:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CartController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_or_create_cart(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        return cart

    def add_item_to_cart(self, cart_id, book_id):
        cart_item = CartItem.query.filter_by(cart_id=cart_id, book_id=book_id).first()

        if cart_item:
            return None
        else:
            # If it doesn't exist, create a new CartItem
            cart_item = CartItem(cart_id=cart_id, book_id=book_id)
            db.session.add(cart_item)

        db.session.commit()

    def remove_item_from_cart(self, cart_item_id):
        cart_item = CartItem.query.get(cart_item_id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return True
        return False

    def get_cart_items(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            return None
        items = CartItem.query.filter_by(cart_id=cart.id).all()
        return items

    def place_order(self, user_id, address, phone_number, book_ids):
        new_order = Order(
            user_id=user_id,
            order_date=datetime.datetime.now(),
            status='Pending',
            address=address,
            phone_number=phone_number
        )

        db.session.add(new_order)
        db.session.commit() 
        for book_id in book_ids:
            order_detail = OrderDetail(
                order_id=new_order.id,
                book_id=book_id
            )
            db.session.add(order_detail)
        db.session.commit()

        return new_order.id 

    def clear_cart(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            # Get all items in the cart
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            for item in cart_items:
                db.session.delete(item)  # Delete each item
            db.session.commit()  # Commit the changes
            return True
        return False

    def fulfill_order(self, order_id):
        order = Order.query.get(order_id)
        if order and order.status == 'Pending':
            order.status = 'Completed'  
            db.session.commit()
            return True
        return False

    def get_orders(self, issued):
        orders = Order.query.filter_by(status="Completed" if issued else "Pending").all()
        if orders:
            return orders
        return None

    def order_details_by_order_id(self, order_id):
        return OrderDetail.query.filter_by(order_id=order_id).all()
