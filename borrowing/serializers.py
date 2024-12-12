from rest_framework import serializers

from borrowing.models import Borrowing, Payments


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


def create(validated_data):
    book = validated_data["book"]
    if book.inventory < 1:
        raise serializers.ValidationError("No more books available")
    book.inventory -= 1
    book.save()
    borrowing = Borrowing.objects.create(**validated_data)
    return borrowing


class BorrowingsDetailSerializer(BorrowingSerializer):
    inventory = serializers.CharField(source="book_id.inventory", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "inventory",
        )


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = (
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay",
        )
