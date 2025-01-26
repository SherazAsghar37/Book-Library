import os
import uuid
from flask import jsonify, url_for
from werkzeug.utils import secure_filename
from app.models.books import Book, db

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads') 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class BookController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BookController, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def create_book(self, form):
        print(form.image_file)
        print(form.title)
        title = form.title.data
        description = form.description.data
        author = form.author.data
        illustrator = form.illustrator.data
        format = form.format.data
        pages = form.pages.data
        quantity = form.quantity.data
        image_file = form.image_file.data
        
        image_url = None
        
        # Handle the image upload
        if image_file and self.allowed_file(image_file.filename):
            # Generate a unique filename using UUID and preserve file extension
            unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            # Ensure the upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            print(UPLOAD_FOLDER)
            print(file_path)
            print(image_file)
            # Save the file
            try:
                image_file.save(file_path)
                print("File saved successfully at:", file_path)
            except Exception as e:
                print("Error saving file:", e)

            image_url = unique_filename
        else:
            return None
        new_book = Book(
            title=title,
            description=description,
            author=author,
            illustrator=illustrator,
            format=format,
            pages=pages,
            quantity=quantity,
            image_url=image_url 
        )
        
        db.session.add(new_book)
        db.session.commit()
        return new_book

    def get_all_books(self):
        return Book.query.all()

    def get_book_by_id(self, book_id):
        return Book.query.get(book_id)

    def delete_book(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True
        return False

    def search_books(self, query):
        return Book.query.filter(
            Book.title.ilike(f'%{query}%') | 
            Book.author.ilike(f'%{query}%')
        ).all()

    def update_book(self, book_id, form):
        book = Book.query.get(book_id)
        
        if book:
            # Update the book attributes with the new values from the form
            if form.title.data:
                book.title = form.title.data
            if form.description.data:
                book.description = form.description.data
            if form.author.data:
                book.author = form.author.data
            if form.illustrator.data:
                book.illustrator = form.illustrator.data
            if form.format.data:
                book.format = form.format.data
            if form.pages.data is not None:
                book.pages = form.pages.data
            if form.quantity.data is not None:
                book.quantity = form.quantity.data
            
            image_file = form.image_file.data
            if image_file and self.allowed_file(image_file.filename):
                # Generate a unique filename using UUID and preserve file extension
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image_file.filename)}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                # Ensure the upload folder exists
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # Save the new image file
                try:
                    image_file.save(file_path)
                    book.image_url = unique_filename  # Update the image_url if the image is uploaded
                except Exception as e:
                    print("Error saving file:", e)

            # Commit the changes to the database
            
            db.session.commit()
            return book

        return None  # Book not found

    def lend_book(self, book_id):
        book = Book.query.get(book_id)
        if book and book.quantity > 0:
            book.quantity -= 1  # Decrease the quantity by 1
            db.session.commit()  # Commit the changes
            return True  # Successfully lent the book
        return False  # Book not found or not available

    def return_book(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.quantity += 1  # Increase the quantity by 1
            db.session.commit()  # Commit the changes
            return True  # Successfully returned the book
        return False  # Book not found
