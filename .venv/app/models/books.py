from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    illustrator = db.Column(db.String(100), nullable=True)
    format = db.Column(db.String(50), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity =  db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True) 


    def __repr__(self):
        return f"<Book {self.title}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "illustrator": self.illustrator,
            "format": self.format,
            "pages": self.pages,
            "quantity":self.quantity,
            "image_url": self.image_url,
        }
