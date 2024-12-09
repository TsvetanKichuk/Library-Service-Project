from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.Serializer):
    class Meta:
        model: Borrowing
        fields = '__all__'
