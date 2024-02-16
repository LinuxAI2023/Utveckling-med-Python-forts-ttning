import unittest
import json
from your_flask_app import app

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)  # Kontrollera att det finns böcker i svaret

    def test_add_book(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "summary": "Test Summary",
            "genre": "Test Genre"
        }
        response = self.app.post('/books', json=book_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'Test Book')

    # Lägg till fler tester för andra endpoints här

if __name__ == '__main__':
    unittest.main()