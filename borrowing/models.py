import datetime

import stripe
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from book_app.models import Book
from mybot.views import send_telegram_notification


class Borrowing(models.Model):
    borrow_date = models.DateField(default=datetime.date.today)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book_id} - {self.user_id}"


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance.user_id, "telegram_id") and instance.user_id.telegram_id:
            message = f"{instance.user_id} added new borrow: {instance.book_id.title}"
            try:
                send_telegram_notification(instance.user_id.telegram_id, message)
            except Exception as e:
                print(f"Error sending telegram notification: {e}")


class Payments(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "pending payments"),
        ("PAYED", "payed payments"),
    ]
    TYPE_CHOICES = [
        ("PAYMENT", "payment"),
        ("FINE", "fine"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.status}"


@receiver(post_save, sender=Payments)
def create_stripe_session(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="payment",
                    line_items=[
                        {
                            "price_data": {
                                "currency": "usd",
                                "product_data": {
                                    "name": f"Payment for borrowing {instance.borrowing_id.book_id.title}",
                                },
                                "unit_amount": int(instance.money_to_pay * 100),  # Stripe требует сумму в центах
                            },
                            "quantity": 1,
                        }
                    ],
                    success_url="https://buy.stripe.com/test_28ocN89fyfPM9NK8wx",
                    cancel_url="https://buy.stripe.com/test_28ocN89fyfPM9NK8wx/cancel",
                )

                instance.session_url = session.url
                instance.session_id = session.id
                instance.save()
        except Exception as e:
            print(f"Error creating stripe session: {e}")
            raise
