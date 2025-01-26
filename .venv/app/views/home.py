from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@main.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


