from os import environ

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

load_dotenv()

MY_TOKEN = environ["TELEGRAM_TOKEN"]

updater = Updater(token=MY_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello I'm your bot!"
    )


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

updater.start_polling()
