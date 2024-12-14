from django.shortcuts import render
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

MY_TOKEN = "7966195586:AAGZo2C8RpUQQ289OHAkeftVKDqbs3kd-ns"

updater = Updater(token=MY_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello I'm your bot!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
