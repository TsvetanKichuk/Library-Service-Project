from book_app.models import Book
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from borrowing.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@user.test", password="password")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=1.99
        )
        self.borrow_date = date.today()
        self.expected_return_date = self.borrow_date + timedelta(days=7)

    def test_str_representation(self):
        borrowing = Borrowing.objects.create(
            borrow_date=self.borrow_date,
            expected_return_date=self.expected_return_date,
            book_id=self.book,
            user_id=self.user
        )
        self.assertEqual(str(borrowing), f"{self.book} - {self.user}")

    def test_create_valid_borrowing(self):
        borrowing = Borrowing.objects.create(
            borrow_date=self.borrow_date,
            expected_return_date=self.expected_return_date,
            book_id=self.book,
            user_id=self.user
        )
        self.assertEqual(borrowing.borrow_date, self.borrow_date)
        self.assertEqual(borrowing.expected_return_date, self.expected_return_date)
        self.assertIsNone(borrowing.actual_return_date)

    def test_expected_return_date_before_borrow_date(self):
        invalid_return_date = self.borrow_date - timedelta(days=1)
        with self.assertRaises(ValueError):
            Borrowing.objects.create(
                borrow_date=self.borrow_date,
                expected_return_date=invalid_return_date,
                book_id=self.book,
                user_id=self.user
            )

    def test_null_actual_return_date(self):
        borrowing = Borrowing.objects.create(
            borrow_date=self.borrow_date,
            expected_return_date=self.expected_return_date,
            book_id=self.book,
            user_id=self.user,
            actual_return_date=None
        )
        self.assertIsNone(borrowing.actual_return_date)

    def test_actual_return_date_not_null(self):
        actual_return_date = self.borrow_date + timedelta(days=5)
        borrowing = Borrowing.objects.create(
            borrow_date=self.borrow_date,
            expected_return_date=self.expected_return_date,
            book_id=self.book,
            user_id=self.user,
            actual_return_date=actual_return_date
        )
        self.assertEqual(borrowing.actual_return_date, actual_return_date)