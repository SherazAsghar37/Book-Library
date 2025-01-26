# app/controllers/forms.py
from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField,EmailField,TelField, PasswordField, BooleanField, DateField, SubmitField,FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    address = StringField('Address')
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    gender = StringField('Gender')
    is_admin = BooleanField('Admin')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    author = StringField('Author', validators=[DataRequired(), Length(max=50)])
    illustrator = StringField('Illustrator', validators=[DataRequired(), Length(max=50)])
    format = StringField('Format', validators=[DataRequired(), Length(max=20)])
    pages = IntegerField('Pages', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image_file = FileField('Image File', validators=[DataRequired()])
    

class AddToCartForm(FlaskForm):
    user_id = HiddenField(validators=[DataRequired()])
    book_id = HiddenField(validators=[DataRequired()])
    action_type = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Shipping Address', validators=[DataRequired(), Length(max=255)])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(max=16)])
    
