from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from borrowing.models import Borrowing, Payments
from borrowing.serializers import (
    BorrowingSerializer,
    PaymentsSerializer,
    BorrowingsDetailSerializer,
)


class BorrowingFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_id__id", lookup_expr="exact")
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Borrowing
        fields = ["user_id", "is_active"]

    def filter_is_active(self, queryset, name, value):
        if value:
            return queryset.filter(returned_at__isnull=True)
        return queryset.filter(returned_at__isnull=False)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user_id", "book_id")
    serializer_class = BorrowingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer
        return BorrowingsDetailSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.select_related("borrowing_id__user_id")
    serializer_class = PaymentsSerializer
