from rest_framework import serializers

from borrowing.models import Borrowing, Payments


class BorrowingSerializer(serializers.Serializer):
    class Meta:
        model: Borrowing
        fields = '__all__'


class PaymentsSerializers(serializers.Serializer):
    class Meta:
        model: Payments
        fields = '__all__'
