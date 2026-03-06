from telebot import TeleBot
from telebot.types import Message
from database.db import get_or_create_user
from keyboards.keyboards import main_menu_keyboard


def register_start_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start", "help"])
    def cmd_start(message: Message):
        user = message.from_user
        get_or_create_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        text = (
            "🌌 <b>Добро пожаловать в CardBlackHole!</b>\n\n"
            "Это карточный бот с космической тематикой.\n"
            "Собирай карточки — от обычной <b>звёздной пыли</b> до легендарных "
            "<b>чёрных дыр</b>!\n\n"
            "⏱ Новую карточку можно открывать каждые <b>2 часа</b>.\n"
            "🕳️ Чёрные дыры выпадают с шансом <b>3%</b> — это редкость!\n\n"
            "Используй меню ниже, чтобы начать:"
        )
        bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())

    @bot.message_handler(commands=["menu"])
    def cmd_menu(message: Message):
        bot.send_message(
            message.chat.id,
            "📋 Главное меню:",
            reply_markup=main_menu_keyboard()
        )
