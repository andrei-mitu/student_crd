from telebot import TeleBot, types
from telebot.types import Message

from database.repository.repositories import UserRepository
from model.entity.user import User
from model.models import Course

userRepo = UserRepository()


def insert_user(message):
    userRepo.insert(User(message.chat.id, message.chat.username, None, message.text))


class Handler:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def configure(self, message):
        self.bot.send_message(message.chat.id, "To continue I need to know your IDNP:")
        self.bot.register_next_step_handler(message, insert_user)

    def get_notes(self, message):
        self.bot.send_message(message.chat.id, "Here are your notes:")
        notes: list[Course] = userRepo.notes(message.chat.id, message.text)
        for course in notes:
            self.bot.send_message(message.chat.id, f"{course.course_name}:", parse_mode='Markdown')
            for note in course.course_notes:
                self.bot.send_message(message.chat.id, f"{note.note_type}: {note.note}")

    def notes(self, message):
        self.bot.send_message(message.chat.id, "Type the semester or skip:",
                              reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                  types.KeyboardButton("Skip")))
        self.bot.register_next_step_handler(message, self.get_notes)

    def welcome(self, message: Message):
        markup = (types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Configure")).add(
            types.KeyboardButton("Notes")))

        if userRepo.exists(message.chat.id):
            self.bot.send_message(message.chat.id, f"Welcome back {message.chat.username}!", reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, "Welcome to One Player Bot!")
            self.bot.send_message(message.chat.id, "Would you like to configure your account?", reply_markup=markup)

    def on_start(self, message):
        self.welcome(message)
