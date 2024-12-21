from django.core.management.base import BaseCommand

from mybot.views import application


class Command(BaseCommand):
    help = "Runs the Telegram bot."

    def handle(self, *args, **options):
        application.start_polling()
