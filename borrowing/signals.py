import asyncio

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from telegram import Bot

from borrowing.models import Borrowing
from payment.models import Payments

MY_TOKEN = settings.TELEGRAM_BOT_API_KEY
CHAT_ID = settings.CHAT_ID


async def async_send_telegram_notification(chat_id, message):
    """
    Asynchronous function to send a message via Telegram bot.
    """
    bot = Bot(token=MY_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)


def send_telegram_notification(chat_id, message):
    """
    Wrapper to run the async function in an asyncio loop.
    """
    asyncio.run(async_send_telegram_notification(chat_id, message))


@receiver(post_save, sender=Borrowing)
def notify_new_borrowing(sender, instance, created, **kwargs):
    if created:
        message = f"New borrowing created: {instance.user_id.email} - {instance.book_id.title}"
        send_telegram_notification(chat_id=CHAT_ID, message=message)


@receiver(post_save, sender=Payments)
def notify_successful_payment(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Payment Successful: Payment of {instance.money_to_pay} "
            f"for borrowing '{instance.borrowing_id.book_id.title}' was successful."
        )
        send_telegram_notification(chat_id=CHAT_ID, message=message)
