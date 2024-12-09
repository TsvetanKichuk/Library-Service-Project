from rest_framework.viewsets import GenericViewSet

from book_app.models import Book
from book_app.permissions import IsAdminOrIfAuthenticatedReadOnly
from book_app.serializers import BookSerializer


class BookViewSet(GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
