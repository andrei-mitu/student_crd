import logging
import os

import telebot
from dotenv import load_dotenv
from telebot import types

from service.telegram import handler

load_dotenv()
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
handler = handler.Handler(bot)
logging.getLogger().setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    handler.on_start(message)


@bot.message_handler(commands=['configure'])
def send_welcome(message):
    handler.configure(message)


@bot.message_handler(func=lambda message: message.text == "Configure")
def send_welcome(message):
    handler.configure(message)


@bot.message_handler(commands=['notes'])
def send_welcome(message):
    handler.notes(message)


@bot.message_handler(func=lambda message: message.text == "Notes")
def send_welcome(message):
    handler.notes(message)


def polling():
    c1 = types.BotCommand(command='start', description='Start the Bot')
    c2 = types.BotCommand(command='notes', description='Check your notes')
    c3 = types.BotCommand(command='configure', description='Configure your account')
    bot.set_my_commands([c1, c2, c3])

    logging.log(logging.INFO, 'Starting bot')
    bot.polling()
