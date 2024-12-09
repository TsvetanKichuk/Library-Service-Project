from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.GenericViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
