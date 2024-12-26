from django.test import TestCase

from django.test import TestCase
from book_app.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=1.99,
        )

    def test_create_book(self):
        book = self.book
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.cover, "HARD")
        self.assertEqual(book.inventory, 10)
        self.assertEqual(book.daily_fee, 1.99)

    def test_invalid_inventory(self):
        """Тест для неверного значения inventory"""
        with self.assertRaises(ValueError):
            Book.objects.create(
                title="Invalid Book",
                author="Author",
                cover="SOFT",
                inventory=-5,  # Неверное значение
                daily_fee=5.9,
            )

    def test_str_representation(self):
        """Тест строкового представления объекта"""
        self.assertEqual(
            str(self.book),
            f"book id: {self.book.id}, '{self.book.title}', (inventory : {self.book.inventory})",
        )
