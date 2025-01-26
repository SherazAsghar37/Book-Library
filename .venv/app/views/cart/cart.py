from flask import jsonify, redirect, request, flash, render_template, session, url_for
from . import cart_bp as cart
from app.controllers.forms import AddToCartForm,CheckoutForm


from app.controllers.books import BookController
from app.controllers.cart import CartController
from app.controllers.user import UserController

user_controller = UserController()
cart_controller = CartController()
book_controller = BookController()

@cart.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    form = AddToCartForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        book_id = form.book_id.data
        action_type = form.action_type.data
        book = book_controller.get_book_by_id(book_id)

    
        cart = cart_controller.get_or_create_cart(user_id)
        print(cart)
        if cart is None:
            flash('Book already added to cart', 'warning')  
        else:
            cart_controller.add_item_to_cart(cart.id,book_id)
            flash('Book added to cart', 'success')  
        return render_template('viewBook.html', book=book, action_type=action_type,form=form)

    
    flash('Failed to add book to cart', 'danger')
    return render_template('viewBook.html', book=book, action_type=action_type,form=form)

@cart.route('/cart_page', methods=['GET'])
def cart_page():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to view your cart.', 'warning')
        return redirect(url_for('auth.login'))  

    
    user_cart =cart_controller.get_or_create_cart(user_id)
    if not user_cart:
        return render_template('cartPage.html', items=[], total=0)

    
    cart_items =cart_controller.get_cart_items(user_id)

    return render_template('cartPage.html', items=cart_items)

@cart.route('/remove_from_cart', methods=['DELETE'])
def remove_from_cart():
    data = request.json
    cart_item_id = data.get('cart_item_id')

    
    cart_item =cart_controller.remove_item_from_cart(cart_item_id)
    if cart_item:
      
        return jsonify({'message': 'Item removed from cart'}), 200
    else:
        return jsonify({'message': 'Item not found in cart'}), 404

@cart.route('/checkout', methods=['GET', 'POST'])
def checkout():
    print("Inside checkout")
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to view your cart.', 'warning')
        return redirect(url_for('auth.login'))  
    form = CheckoutForm()
    if form.validate_on_submit():
        print("Inside checkout1")
        
        
        cart_items = cart_controller.get_cart_items(user_id)
        print(cart_items)
        if not cart_items:
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('cart.cart_page'))  
        print("cart_items")
        
        all_books_lent = True
        for item in cart_items:
            if not book_controller.lend_book(item.book_id):  
                all_books_lent = False
                flash(f'Could not lend book: {item.book.title}', 'danger')
        print("cart_items1")
        

        if not all_books_lent:
            return redirect(url_for('cart.cart_page'))  

        
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        card_number = form.card_number.data
        

        book_ids = [item.book_id for item in cart_items] 
        order_id = cart_controller.place_order(user_id, address, phone, book_ids)

        if order_id:
            cart_controller.clear_cart(user_id)  
            flash('Order placed successfully!', 'success')
            return redirect(url_for('main.home'))  

    return render_template('checkout.html', form=form)

@cart.route('/fulfill_order/<int:order_id>', methods=['GET'])
def fulfill_order(order_id):
    if cart_controller.fulfill_order(order_id):
        flash('Order filfilled successfully!', 'success')
        return redirect(url_for('cart.view_orders',issued="false"))
    flash('Something went wrong unable to fullfil the order!', 'danger')      
    return redirect(url_for('cart.view_orders',issued="false"))

@cart.route('/view_orders/<string:issued>', methods=['GET'])
def view_orders(issued):
    isIssued=issued=="true"
    orders = cart_controller.get_orders(isIssued)
    order_details = []
    if orders!=None:
        for order in orders:
            user = user_controller.get_user_by_id(order.user_id)
            order_items  = cart_controller.order_detials_by_order_id(order.id)
            for item in order_items:
                    book =book_controller.get_book_by_id(item.book_id)
                    order_details.append({
                        'user': user,
                        'order': order,
                        'book': book
                    })
    else:
        flash('No orders found', 'danger')     

    return render_template('orders.html', order_details=order_details,issued = issued)
    