from rest_framework import viewsets

from borrowing.models import Borrowing, Payments
from borrowing.serializers import BorrowingSerializer, PaymentsSerializers


class BorrowingViewSet(viewsets.GenericViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class PaymentsViewSet(viewsets.GenericViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializers
