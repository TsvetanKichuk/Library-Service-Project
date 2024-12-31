from book_app.models import Book
from borrowing.models import Borrowing
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from borrowing.serializers import BorrowingSerializer


class BorrowingSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@user.net", password="testpassword")
        self.book = Book.objects.create(title="Test Book", author="Author", inventory=1)
        self.borrowing_data = {
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=7),
            "book_id": self.book.id,
            "user_id": self.user.id,
        }

    def test_create_valid_borrowing(self):
        serializer = BorrowingSerializer(data=self.borrowing_data)
        self.assertTrue(serializer.is_valid())
        borrowing = serializer.save()
        self.assertEqual(borrowing.book_id, self.book)
        self.assertEqual(borrowing.user_id, self.user)
        self.assertEqual(self.book.inventory, 1)

    def test_create_borrowing_with_no_inventory(self):
        self.book.inventory = 0
        self.book.save()
        serializer = BorrowingSerializer(data=self.borrowing_data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_borrowing_with_return_date(self):
        borrowing = Borrowing.objects.create(**self.borrowing_data)
        update_data = {
            "actual_return_date": date.today()
        }
        serializer = BorrowingSerializer(instance=borrowing, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_borrowing = serializer.save()
        self.assertEqual(updated_borrowing.actual_return_date, date.today())
        self.assertEqual(self.book.inventory, 2)

    def test_update_borrowing_that_is_already_returned(self):
        borrowing = Borrowing.objects.create(**self.borrowing_data, actual_return_date=date.today())
        update_data = {
            "actual_return_date": date.today()
        }
        serializer = BorrowingSerializer(instance=borrowing, data=update_data, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
