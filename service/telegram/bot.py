import logging
import os

import telebot
from dotenv import load_dotenv

from service.telegram import handler

load_dotenv()
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
handler = handler.Handler(bot)
logging.getLogger().setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    handler.on_start(message)


@bot.message_handler(func=lambda message: message.text == "Configure")
def send_welcome(message):
    handler.configure(message)


@bot.message_handler(func=lambda message: message.text == "Notes")
def send_welcome(message):
    handler.notes(message)


def polling():
    logging.log(logging.INFO, 'Starting bot')
    bot.polling()
