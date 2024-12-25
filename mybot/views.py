from dotenv import load_dotenv
from telegram import Bot
import telebot
from telegram.ext import Application, CommandHandler

import mybot
from library_service_project import settings

load_dotenv()

MY_TOKEN = settings.TELEGRAM_BOT_API_KEY

application = Application.builder().token(MY_TOKEN).build()


async def start(update, context):
    await update.message.reply_text("Hello I'm your library project bot!")


def send_telegram_notification(chat_id, message):
    bot = Bot(token=MY_TOKEN)
    bot.send_message(chat_id=chat_id, text=message)


start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

application.run_polling()
