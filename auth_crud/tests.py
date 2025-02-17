# python -m unittest test_basic_memory_crud.py

import unittest
import json
from crud_memory import app, books

class BasicMemoryCrudTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset the in-memory storage before each test
        global books
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

    def tearDown(self):
        # Clean up any resources or reset states if necessary
        global books
        books = []  # Clear the books list after each test

    def test_get_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)

    def test_add_book(self):
        new_book = {
            'title': '1984',
            'author': 'George Orwell',
            'year': 1949
        }
        response = self.app.post('/books', json=new_book)
        self.assertEqual(response.status_code, 201)
        self.assertIn('1984', str(response.data))

    def test_get_book(self):
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('The Great Gatsby', str(response.data))

    def test_update_book(self):
        updated_book = {
            'title': 'The Great Gatsby - Updated'
        }
        response = self.app.put('/books/1', json=updated_book)
        self.assertEqual(response.status_code, 200)
        self.assertIn('The Great Gatsby - Updated', str(response.data))

    def test_delete_book(self):
        response = self.app.delete('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted', str(response.data))

    def test_delete_book_not_found(self):
        response = self.app.delete('/books/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Book not found', str(response.data))

    def test_get_book_not_found(self):
        response = self.app.get('/books/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Book not found', str(response.data))

if __name__ == '__main__':
    # Create a test suite and add tests in the desired order
    suite = unittest.TestSuite()
    suite.addTest(BasicMemoryCrudTests('test_get_books'))
    suite.addTest(BasicMemoryCrudTests('test_add_book'))
    suite.addTest(BasicMemoryCrudTests('test_get_book'))
    suite.addTest(BasicMemoryCrudTests('test_update_book'))
    suite.addTest(BasicMemoryCrudTests('test_delete_book'))
    suite.addTest(BasicMemoryCrudTests('test_delete_book_not_found'))
    suite.addTest(BasicMemoryCrudTests('test_get_book_not_found'))

    runner = unittest.TextTestRunner()
    runner.run(suite) 