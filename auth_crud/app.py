from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# In-memory storage for books
books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960
    }
]

# Dummy user data for authentication
users = {
    "admin": "123",  # username: admin, password: password123
}

# Verify the username and password
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Get all books
@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify(books)

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

# Add a new book
@app.route('/books', methods=['POST'])
@auth.login_required
def add_book():
    if not request.json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    new_book = {
        'id': max(book['id'] for book in books) + 1,
        'title': request.json.get('title'),
        'author': request.json.get('author'),
        'year': request.json.get('year')
    }
    
    books.append(new_book)
    return jsonify(new_book), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['year'] = request.json.get('year', book['year'])
    
    return jsonify(book)

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    books.remove(book)
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)