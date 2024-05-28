from telebot import TeleBot, types
from telebot.types import Message

from database.repository.repositories import UserRepository
from model.entity.user import User
from model.models import Note

userRepo = UserRepository()


def insert_user(message):
    userRepo.insert(User(message.chat.id, message.chat.username, None, message.text))


class Handler:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def configure(self, message):
        self.bot.send_message(message.chat.id, "To continue I need to know your IDNP:")
        self.bot.register_next_step_handler(message, insert_user)
        self.bot.register_next_step_handler(message, self.on_start)

    def get_notes(self, message):
        text_message = ""
        notes: list[Note] = userRepo.notes(message.chat.id, message.text)
        semester = message.text if message.text is not None and message.text != 'Skip' else 'last'
        self.bot.send_message(message.chat.id, f"Here are your notes for {semester} semester:")
        for note in notes:
            text_message += f"{note.note_type}: {note.note}\n"
        self.bot.send_message(message.chat.id, text_message,
                              reply_markup=types.ReplyKeyboardRemove())

    def notes(self, message):
        self.bot.send_message(message.chat.id, "Type the semester or skip:",
                              reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                  types.KeyboardButton("Skip")))
        self.bot.register_next_step_handler(message, self.get_notes)

    def welcome(self, message: Message):
        exists = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Notes"))
        new = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Notes")).add(
            types.KeyboardButton("Configure"))
        if userRepo.exists(message.chat.id):
            self.bot.send_message(message.chat.id, f"Welcome back {message.chat.username}!", reply_markup=exists)
        else:
            self.bot.send_message(message.chat.id, "Welcome to Student Crd Bot!")
            self.bot.send_message(message.chat.id, "Would you like to configure your account?", reply_markup=new)

    def on_start(self, message):
        self.welcome(message)
