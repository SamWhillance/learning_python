from flask import Flask, jsonify, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Dummy user data for authentication
users = {
    "admin": "123",  # username: admin, password: password123
}

# Verify the username and password
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Get all books (no auth required)
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year} for book in books])

# Get a single book by ID (no auth required)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

# Add a new book
@app.route('/books', methods=['POST'])
@auth.login_required
def add_book():
    if not request.json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    new_book = Book(
        title=request.json.get('title'),
        author=request.json.get('author'),
        year=request.json.get('year')
    )
    
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'year': new_book.year}), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.year = request.json.get('year', book.year)
    
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year})

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)