from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from book_app.models import Book
from book_app.permissions import IsAdminOrIfAuthenticatedReadOnly
from book_app.serializers import BookSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = OrderPagination
