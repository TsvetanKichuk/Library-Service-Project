from celery import shared_task
from dateutil.utils import today
from django.db.models import Q

from borrowing.models import Borrowing
from borrowing.signals import send_telegram_notification


@shared_task
def check_overdue_borrowings():
    overdue_borrowings = Borrowing.objects.filter(
        Q(expected_return_date__lte=today) & Q(returned_at__isnull=True)
    )

    for borrowing in overdue_borrowings:
        message = (
            f"Overdue Borrowing Alert:\n"
            f"Book: {borrowing.book_id.title}\n"
            f"Due Date: {borrowing.expected_return_date}\n"
            f"Please return your book to avoid penalties."
        )
        try:
            send_telegram_notification(borrowing.user_id.email, message)
        except Exception as e:
            print(f"Error while sending overdue borrowing notification: {e}")
