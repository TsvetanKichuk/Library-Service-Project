from django.core.management.base import BaseCommand
from mybot.views import updater


class Command(BaseCommand):
    help = 'Runs the Telegram bot.'

    def handle(self, *args, **options):
        updater.start_polling()
