import os

import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY

stripe.Customer.create(
    name="Tsvetan Kichuk",
    email="toys4babyodua@gmail.com",
)

stripe.PaymentIntent.create(
    customer='{{CUSTOMER_ID}}',
    amount=1099,
    currency="usd",
    setup_future_usage="off_session",
    automatic_payment_methods={"enabled": True},
)

stripe.Balance.retrieve(stripe_account='{{CONNECTED_ACCOUNT_ID}}')

stripe.Product.list(
    limit=5,
    stripe_account='{{CONNECTED_ACCOUNT_ID}}',
)

stripe.Customer.delete(
    "{{CUSTOMER_ID}}",
    stripe_account='{{CONNECTED_ACCOUNT_ID}}',
)

