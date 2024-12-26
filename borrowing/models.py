import datetime

from django.conf import settings
from django.db import models

from book_app.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(default=datetime.date.today)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book_id} - {self.user_id}"

    def save(self, *args, **kwargs):
        if self.expected_return_date < self.borrow_date:
            raise ValueError("Expected return date cannot be before borrow date.")
        super().save(*args, **kwargs)
