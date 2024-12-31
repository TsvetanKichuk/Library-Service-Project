from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        if "actual_return_date" in validated_data and not instance.actual_return_date:
            instance.actual_return_date = validated_data["actual_return_date"]

            book = instance.book_id
            book.inventory += 1
            book.save()
        elif instance.actual_return_date:
            raise serializers.ValidationError(
                "Cannot update a borrowing record that is already returned."
            )

        for attr, value in validated_data.items():
            if (
                attr != "actual_return_date"
            ):
                setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, data):
        if self.instance and self.instance.actual_return_date:
            raise ValidationError(
                "Cannot update a borrowing record that is already returned."
            )
        return data


class BorrowingsDetailSerializer(BorrowingSerializer):
    book = BookSerializer(
        source="book_id",
        read_only=True,
    )

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
