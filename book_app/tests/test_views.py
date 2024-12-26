from book_app.models import Book
from book_app.serializers import BookSerializer, BookDetailSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class BookViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            cover="HARD",
            inventory=5,
            daily_fee=1.50,
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            cover="SOFT",
            inventory=2,
            daily_fee=2.00,
        )

    def test_list_books(self):
        url = reverse('books-list')
        response = self.client.get(url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_books_by_title(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?title=Book One")
        serializer = BookSerializer([self.book1], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_books_by_author(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?author={self.book1.author}")
        serializer = BookSerializer([self.book1], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_unauthenticated(self):
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 3,
            "daily_fee": 1.99,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_unauthenticated(self):
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            "title": "Updated Title",
            "author": self.book1.author,
            "cover": self.book1.cover,
            "inventory": self.book1.inventory,
            "daily_fee": self.book1.daily_fee,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_unauthenticated(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)