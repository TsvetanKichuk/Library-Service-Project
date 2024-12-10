from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from book_app.models import Book
from book_app.permissions import IsAdminOrIfAuthenticatedReadOnly
from book_app.serializers import BookSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BookViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = OrderPagination

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
