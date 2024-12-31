from book_app.models import Book
from borrowing.models import Borrowing
from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from payment.models import Payments
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class PaymentsViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@user.net", password="password123")
        self.admin_user = User.objects.create_superuser(email="admin@test.com", password="admin123")
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            cover="Hardcover",
            inventory=10,
            daily_fee=1.99,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            user_id=self.user,
            book_id=self.book,
        )
        self.payment = Payments.objects.create(
            borrowing_id=self.borrowing,
            status="Pending",
            type="Card",
            money_to_pay=100.0,
        )

    def test_get_payments_list_unauthenticated(self):
        response = self.client.get(reverse('payments:payments-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_payments_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('payments:payments-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_payments_list_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('payments:payments-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment_unauthenticated(self):
        response = self.client.post(reverse('payments:payments-list'), data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_payment_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('payments:payments-list'), data={
            "borrowing_id": self.borrowing.id,
            "status": "Pending",
            "type": "Card",
            "amount": 50.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_payment_detail_unauthenticated(self):
        response = self.client.get(reverse('payments:payments-detail', args=[self.payment.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_payment_detail_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('payments:payments-detail', args=[self.payment.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_payment_detail_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('payments:payments-detail', args=[self.payment.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_payment_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(reverse('payments:payments-detail', args=[self.payment.id]), data={
            "status": "Completed"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_payment_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(reverse('payments:payments-detail', args=[self.payment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_payment_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('payments:payments-detail', args=[self.payment.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
