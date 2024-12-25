from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from book_app.models import Book
from permissions import IsAdminOrIfAuthenticatedReadOnly
from book_app.serializers import BookSerializer, BookDetailSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = OrderPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookSerializer
        return BookDetailSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "author",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by author id (ex. ?actors=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by book title (ex. ?title=fiction)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
