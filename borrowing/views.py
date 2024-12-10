from rest_framework import viewsets, status
from rest_framework.response import Response

from borrowing.models import Borrowing, Payments
from borrowing.serializers import BorrowingSerializer, PaymentsSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user_id", "book_id")
    serializer_class = BorrowingSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = BorrowingSerializer(data=request.data)

        if serializer.is_valid():
            book = serializer.validated_data["book_id"]

            if book.inventory > 0:
                book.inventory -= 1
                book.save()

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Book is not available"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.select_related("borrowing_id")
    serializer_class = PaymentsSerializer
