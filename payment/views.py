import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets

from borrowing.permissions import IsAdminUserOrReadOnly
from payment.models import Payments
from payment.serializers import PaymentsSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY

YOUR_DOMAIN = "http://127.0.0.1:8000"


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.select_related("borrowing_id__user_id")
    serializer_class = PaymentsSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1QZsmuRwyw2Mr9VCS6s4VbFs",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})
