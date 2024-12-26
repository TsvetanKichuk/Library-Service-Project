from django.db import models

from borrowing.models import Borrowing


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
        return f"{self.status}, {self.type}, {self.borrowing_id}"
