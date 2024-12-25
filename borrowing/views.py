from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingsDetailSerializer,
)


class BorrowingFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_id__id", lookup_expr="exact")
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Borrowing
        fields = ["user_id", "is_active"]

    def filter_is_active(self, queryset, user_id, value):
        if value:
            return queryset.filter(expected_return_date__isnull=True)
        return queryset.filter(expected_return_date__isnull=False)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user_id", "book_id")
    serializer_class = BorrowingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer
        return BorrowingsDetailSerializer

    def get_active_user(self, request):
        user_id = request.query_params.get("user_id")
        is_active = request.query_params.get("is_active")

        if user_id is None or is_active is None:
            return Response(
                {
                    "error": "Both 'user_id' and 'is_active' query parameters are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            is_active = is_active.lower() == "true"

            if is_active:
                borrowings = Borrowing.objects.filter(
                    Q(user_id=user_id) & Q(actual_return_date__isnull=True)
                )
            else:
                borrowings = Borrowing.objects.filter(
                    Q(user_id=user_id) & Q(actual_return_date__isnull=False)
                )

            serializer = BorrowingSerializer(borrowings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "book_id",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by book id (ex. ?book=2)",
            ),
            OpenApiParameter(
                "borrow_date",
                type=OpenApiTypes.DATE,
                description="Filter by borrow date (ex. ?borrow_date=2024-12-25)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
