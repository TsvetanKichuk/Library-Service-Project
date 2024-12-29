from datetime import date

from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingsDetailSerializer,
)


class BorrowingFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Borrowing
        fields = ["user_id", "is_active"]

    def filter_is_active(self, queryset, user_id, value):
        if value:
            return queryset.filter(actual_return_date__isnull=True)
        return queryset.filter(actual_return_date__isnull=False)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user_id", "book_id")
    serializer_class = BorrowingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer
        return BorrowingsDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

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


# borrowing/views.py
class ReturnBorrowingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, borrowing_id):
        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist:
            raise NotFound("Borrowing not found.")

        if borrowing.actual_return_date is not None:
            raise ValidationError({"detail": "This borrowing has already been returned."})

        borrowing.actual_return_date = date.today()
        borrowing.save()

        return Response({"message": "Borrowing returned successfully."})
