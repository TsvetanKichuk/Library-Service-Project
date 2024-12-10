from rest_framework import serializers

from borrowing.models import Borrowing, Payments


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model: Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model: Payments
        fields = (
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay",
        )
