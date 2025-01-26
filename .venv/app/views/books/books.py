from flask import Blueprint, redirect, render_template, url_for, flash, session
from app.controllers.forms import BookForm
from app.controllers.books import create_book, get_all_books, get_book_by_id, update_book  # Ensure you have this import
from app.views.books import books_bp as books

UPLOAD_FOLDER = 'static/images/'  # Ensure this path is correct
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@books.route('/getBooks/<string:action_type>', methods=['GET'])
def getBooks(action_type):
    books = get_all_books()
    return render_template('books.html', books=books, action_type=action_type)

@books.route('/add_book/<int:book_id>/<string:action_type>', methods=['GET', 'POST'])
def add_book(book_id, action_type):
    is_edit = action_type=="edit"
    if session.get("is_admin"):  
        form = BookForm()
        if form.validate_on_submit():
            new_book = None
            if is_edit:
                print('Herer')
                new_book = update_book(book_id, form)
            else:
                new_book = create_book(form)
            if not new_book:
                flash('Something went wrong. Unable to add book.', 'danger')
                return render_template('addBook.html', form=form)
            flash('Book added successfully', 'success')
            return redirect(url_for('books.book_detail', book_id=new_book.id, action_type="view"))  
        print('Here2')
        return render_template('addBook.html', form=form,book_id=book_id,action_type=action_type)
    else:
        flash('This action cannot be performed', 'danger')
    return redirect(url_for('main.home'))  # Redi

@books.route('/book_detail/<int:book_id>/<string:action_type>', methods=['GET'])
def book_detail(book_id, action_type):
    print(action_type)
    book = get_book_by_id(book_id)
    if book is None:
        flash('Book not found', 'danger')  
        return redirect(url_for('books.getBooks', action_type="view")) 

    return render_template('viewBook.html', book=book, action_type=action_type)  
