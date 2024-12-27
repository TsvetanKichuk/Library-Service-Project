from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from book_app.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer
from borrowing.views import BorrowingFilter
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django_filters.rest_framework import FilterSet

User = get_user_model()


class BorrowingFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@user.net", password="password123"
        )
        self.book = Book.objects.create(title="Test Book", author="Author")
        self.borrowing1 = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=14),
            actual_return_date=None,
            user_id=self.user,
            book_id=self.book
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date.today() - timedelta(days=20),
            expected_return_date=date.today() - timedelta(days=10),
            actual_return_date=date.today(),
            user_id=self.user,
            book_id=self.book
        )

    def test_filter_by_user_id(self):
        filter_set = BorrowingFilter(
            {"user_id": self.user.id}, Borrowing.objects.all()
        )
        filtered_query = filter_set.qs
        self.assertEqual(filtered_query.count(), 2)
        self.assertIn(self.borrowing1, filtered_query)
        self.assertIn(self.borrowing2, filtered_query)

    def test_filter_is_active_true(self):
        filter_set = BorrowingFilter(
            {"is_active": True}, Borrowing.objects.all()
        )
        filtered_query = filter_set.qs
        self.assertEqual(filtered_query.count(), 1)
        self.assertIn(self.borrowing1, filtered_query)
        self.assertNotIn(self.borrowing2, filtered_query)

    def test_filter_is_active_false(self):
        filter_set = BorrowingFilter(
            {"is_active": False}, Borrowing.objects.all()
        )
        filtered_query = filter_set.qs
        self.assertEqual(filtered_query.count(), 1)
        self.assertNotIn(self.borrowing1, filtered_query)
        self.assertIn(self.borrowing2, filtered_query)


# User = get_user_model()


class GetActiveUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@user.net", password="testpassword123"
        )

        # Create Book objects
        self.book1 = Book.objects.create(title="Book 1", author="Author 1")
        self.book2 = Book.objects.create(title="Book 2", author="Author 2")

        self.borrowing1 = Borrowing.objects.create(
            borrow_date=date(2023, 11, 1),
            expected_return_date=date(2023, 11, 15),
            actual_return_date=None,
            user_id=self.user,
            book_id=self.book1,  # Correct assignment of Book object
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date(2023, 10, 1),
            expected_return_date=date(2023, 10, 15),
            actual_return_date=date(2023, 10, 14),
            user_id=self.user,
            book_id=self.book2,  # Correct assignment of Book object
        )
        self.url = reverse(
            "borrowing-list"
        )  # Replace with correct view name if needed.

    def test_get_active_user_with_missing_parameters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Both 'user_id' and 'is_active' query parameters are required.",
        )

    def test_get_active_user_active_borrowings(self):
        response = self.client.get(
            self.url, {"user_id": self.user.id, "is_active": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        active_borrowings = Borrowing.objects.filter(
            user_id=self.user, actual_return_date__isnull=True
        )
        serializer = BorrowingSerializer(active_borrowings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_active_user_inactive_borrowings(self):
        response = self.client.get(
            self.url, {"user_id": self.user.id, "is_active": "false"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inactive_borrowings = Borrowing.objects.filter(
            user_id=self.user, actual_return_date__isnull=False
        )
        serializer = BorrowingSerializer(inactive_borrowings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_active_user_invalid_is_active_value(self):
        response = self.client.get(
            self.url, {"user_id": self.user.id, "is_active": "invalid"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowings = Borrowing.objects.none()
        serializer = BorrowingSerializer(borrowings, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_active_user_with_nonexistent_user(self):
        response = self.client.get(self.url, {"user_id": 999, "is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowings = Borrowing.objects.filter(
            user_id=999, actual_return_date__isnull=True
        )
        serializer = BorrowingSerializer(borrowings, many=True)
        self.assertEqual(response.data, serializer.data)
