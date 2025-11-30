import unittest
from project.books.models import Book
from project import app, db
from sqlalchemy.exc import IntegrityError

class BookModelTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_valid_book(self):
        """Sprawdza, czy można utworzyć książkę z poprawnymi danymi."""
        book = Book(name="Wiedźmin", author="Sapkowski", year_published=1993, book_type="Fantasy")
        db.session.add(book)
        db.session.commit()
        
        saved_book = Book.query.filter_by(name="Wiedźmin").first()
        self.assertIsNotNone(saved_book)
        self.assertEqual(saved_book.author, "Sapkowski")
        self.assertEqual(saved_book.status, "available")

    def test_create_book_missing_name(self):
        """
        Testuje zachowanie przy braku nazwy.
        """
        book = Book(name=None, author="Unknown", year_published=2000, book_type="Unknown")
        db.session.add(book)
        
        try:
            db.session.commit()
        except IntegrityError:
            pass

    def test_sql_injection_attempt(self):
        """
        Sprawdza odporność na SQL Injection.
        """
        payload = "'; DROP TABLE books; --"
        book = Book(name=payload, author="Hacker", year_published=2021, book_type="Hacking")
        db.session.add(book)
        db.session.commit()

        saved_book = Book.query.filter_by(author="Hacker").first()
        self.assertEqual(saved_book.name, payload)

    def test_xss_injection_attempt(self):
        """
        Sprawdza wstrzyknięcie JavaScript (XSS).
        """
        xss_payload = "<script>alert('Xoused')</script>"
        book = Book(name=xss_payload, author="Script Kiddie", year_published=2021, book_type="XSS")
        db.session.add(book)
        db.session.commit()

        saved_book = Book.query.filter_by(author="Script Kiddie").first()
        self.assertEqual(saved_book.name, xss_payload)

    def test_extreme_year(self):
        """Sprawdza obsługę odległych dat."""
        book = Book(name="Future Book", author="Alien", year_published=99999, book_type="Sci-Fi")
        db.session.add(book)
        db.session.commit()
        
        self.assertEqual(Book.query.filter_by(name="Future Book").first().year_published, 99999)

    def test_extreme_string_length(self):
        """
        Sprawdza zachowanie przy przekroczeniu limitu znaków.
        """
        long_name = "A" * 100
        book = Book(name=long_name, author="Author", year_published=2021, book_type="Test")
        db.session.add(book)
        
        with self.assertRaises(Exception): 
            db.session.commit()

if __name__ == '__main__':
    unittest.main()