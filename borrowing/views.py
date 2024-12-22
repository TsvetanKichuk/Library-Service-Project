import stripe

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.response import Response

from borrowing.models import Borrowing, Payments
from borrowing.permissions import IsAdminOrOwner
from borrowing.serializers import (
    BorrowingSerializer,
    PaymentsSerializer,
    BorrowingsDetailSerializer,
)
from mybot.views import send_telegram_notification


class BorrowingFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_id__id", lookup_expr="exact")
    is_active = filters.BooleanFilter(method="filter_is_active")

    class Meta:
        model = Borrowing
        fields = ["user_id", "is_active"]

    def filter_is_active(self, queryset, name, value):
        if value:
            return queryset.filter(expected_return_date__isnull=True)
        return queryset.filter(expected_return_date__isnull=False)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user_id", "book_id")
    serializer_class = BorrowingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BorrowingFilter

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer
        return BorrowingsDetailSerializer

    def get_active_user(self, request):
        user_id = request.query_params.get("user_id")
        is_active = request.query_params.get("is_active")

        if user_id is None or is_active is None:
            return Response(
                {
                    "error": "Both 'user_id' and 'is_active' query parameters are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            is_active = is_active.lower() == "true"

            if is_active:
                borrowings = Borrowing.objects.filter(
                    Q(user_id=user_id) & Q(actual_return_date__isnull=True)
                )
            else:
                borrowings = Borrowing.objects.filter(
                    Q(user_id=user_id) & Q(actual_return_date__isnull=False)
                )

            serializer = BorrowingSerializer(borrowings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.select_related("borrowing_id__user_id")
    serializer_class = PaymentsSerializer
    permission_classes = IsAdminOrOwner

    def post(self, request):
        serializer = PaymentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            charge = stripe.Charge.create(
                amount=serializer.validated_data['amount'],
                currency='usd',
                source=serializer.validated_data['token'],
            )
            return Response({'charge_id': charge.id})
        except stripe.error.CardError as e:
            return Response({'error': e.user_message})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = "your-webhook-signing-secret"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment = Payments.objects.get(session_id=session["id"])
        payment.status = "PAYED"
        payment.save()
        message = f"{payment.money_to_pay}$ success. Book: '{payment.borrowing_id.book_id.title}'"
        send_telegram_notification(payment.borrowing_id.user_id.telegram_id, message)

    return JsonResponse({"status": "success"})
