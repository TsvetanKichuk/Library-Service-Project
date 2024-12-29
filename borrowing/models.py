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

    def return_borrowing(self):
        if self.actual_return_date:
            raise ValueError("This borrowing has already been returned.")
        self.actual_return_date = datetime.date.today()
        self.book_id.inventory += 1  # Increment book inventory
        self.book_id.save()
        self.save()
