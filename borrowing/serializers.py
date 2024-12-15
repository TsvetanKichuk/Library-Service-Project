from datetime import datetime

from rest_framework import serializers

from book_app.serializers import BookSerializer
from borrowing.models import Borrowing, Payments


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


def create(validated_data):
    book = validated_data["book_id"]
    if book.inventory < 1:
        raise serializers.ValidationError("No more books available")
    book.inventory -= 1
    book.save()
    borrowing = Borrowing.objects.create(**validated_data)
    return borrowing


def return_book(validated_data):
    book = validated_data["book_id"]
    borrowing = validated_data["borrowing_id"]
    if borrowing.actual_return_date is not datetime.date.today():
        return book.inventory
    book.inventory += 1
    book.save()


class BorrowingsDetailSerializer(BorrowingSerializer):
    inventory = BookSerializer(source="book_id", read_only=True, )

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
    money_to_pay = serializers.DecimalField(source=Payments.money_to_pay, max_digits=10, decimal_places=2)

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
