import unittest
from project.books.models import Book

class BookModelTestCase(unittest.TestCase):
    
    def test_create_book_attributes(self):
        """Testuje czy obiekt Book poprawnie przypisuje przekazane atrybuty."""
        book = Book(
            name="Wiedźmin", 
            author="Andrzej Sapkowski", 
            year_published=1993, 
            book_type="Fantasy"
        )
        
        self.assertEqual(book.name, "Wiedźmin")
        self.assertEqual(book.author, "Andrzej Sapkowski")
        self.assertEqual(book.year_published, 1993)
        self.assertEqual(book.book_type, "Fantasy")

    def test_default_status(self):
        """Testuje czy pole status otrzymuje domyślną wartość 'available'."""
        book = Book("Test Book", "Author", 2020, "Test Type")
        self.assertEqual(book.status, "available")

    def test_book_repr(self):
        """Testuje metodę __repr__ zwracającą string z opisem obiektu."""
        book = Book("Test Book", "Author", 2020, "Test Type")
        book.id = 1 
        
        expected_repr = "Book(ID: 1, Name: Test Book, Author: Author, Year Published: 2020, Type: Test Type, Status: available)"
        self.assertEqual(str(book), expected_repr)

if __name__ == '__main__':
    unittest.main()