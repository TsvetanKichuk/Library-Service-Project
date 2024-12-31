from rest_framework import serializers

from book_app.models import Book


class BookSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('id',)


class BookDetailSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("title", "author", "cover", "inventory", "daily_fee")
