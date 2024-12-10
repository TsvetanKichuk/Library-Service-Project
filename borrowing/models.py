import datetime

from django.db import models
from rest_framework.authtoken.admin import User
from book_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(datetime.date.today())
    expected_return_date = models.DateField(datetime.date)
    actual_return_date = models.DateField(datetime.date, null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book_id} - {self.user_id}'


class Payments(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'pending payments'),
        ('PAYED', 'payed payments'),
    ]
    TYPE_CHOICES = [
        ('PAYMENT', 'payment'),
        ('FINE', 'fine'),
    ]
    status = models.BooleanField(choices=STATUS_CHOICES)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.borrowing_id} - {self.status}'
