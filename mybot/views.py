import os

from telegram import Bot

from dotenv import load_dotenv

from telegram.ext import Application, CommandHandler

load_dotenv()

MY_TOKEN = os.environ["TELEGRAM_TOKEN"]

application = Application.builder().token(MY_TOKEN).build()


async def start(update, context):
    await update.message.reply_text("Hello I'm your bot!")


def send_telegram_notification(chat_id, message):
    bot = Bot(token=MY_TOKEN)
    bot.send_message(chat_id=chat_id, text=message)


start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

application.run_polling()
