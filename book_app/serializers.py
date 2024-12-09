from rest_framework import serializers

from book_app.models import Book


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'cover',
            "inventory",
            "daily_fee"
        )
