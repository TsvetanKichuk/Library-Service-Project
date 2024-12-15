from os import environ

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

load_dotenv()

MY_TOKEN = environ["TELEGRAM_TOKEN"]

application = Application.builder().token(MY_TOKEN).build()


async def start(update, context):
    await update.message.reply_text("Hello I'm your bot!")


start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

application.run_polling()
