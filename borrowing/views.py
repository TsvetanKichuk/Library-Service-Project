from rest_framework import viewsets

from borrowing.models import Borrowing, Payments
from borrowing.serializers import BorrowingSerializer, PaymentsSerializers


class BorrowingViewSet(viewsets.GenericViewSet):
    queryset = Borrowing.objects.select_related("book, user")
    serializer_class = BorrowingSerializer


class PaymentsViewSet(viewsets.GenericViewSet):
    queryset = Payments.objects.select_related("borrowing_id")
    serializer_class = PaymentsSerializers
