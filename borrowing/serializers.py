from datetime import date

from rest_framework import serializers

from book_app.serializers import BookSerializer
from borrowing.models import Borrowing


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

    def create(self, validated_data):
        book = validated_data["book_id"]
        if book.inventory < 1:
            raise serializers.ValidationError("No more books available")
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing

    def update(self, instance, validated_data):
        if not instance.actual_return_date:
            raise serializers.ValidationError(
                "This borrowing record is already borrowed."
            )

        instance.actual_return_date = date.today()
        instance.save()
        book = instance.book_id
        book.inventory += 1
        book.save()

        return instance


class BorrowingsDetailSerializer(BorrowingSerializer):
    book = BookSerializer(source="book_id", read_only=True, )

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "book",
        )
