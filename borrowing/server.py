import stripe
from dotenv import load_dotenv
import os

load_dotenv()

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

stripe.PaymentIntent.create(
    amount=1000,
    currency="usd",
    stripe_account="{{CONNECTED_ACCOUNT_ID}}",
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
