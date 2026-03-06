from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import WEBAPP_URL


def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🃏 Открыть карточку"),
        KeyboardButton("📦 Моя коллекция"),
        KeyboardButton("🏆 Топ игроков"),
        KeyboardButton("ℹ️ О боте"),
    )
    return markup


def open_card_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🃏 Открыть карточку!", callback_data="open_card"))
    return markup


def collection_keyboard(user_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            "🌐 Открыть коллекцию в WebApp",
            web_app={"url": f"{WEBAPP_URL}/collection?user_id={user_id}"}
        ),
        InlineKeyboardButton("🔄 Обновить", callback_data="my_collection"),
    )
    return markup


def back_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu"))
    return markup


def after_card_keyboard(user_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📦 Моя коллекция", callback_data="my_collection"),
        InlineKeyboardButton(
            "🌐 WebApp",
            web_app={"url": f"{WEBAPP_URL}/collection?user_id={user_id}"}
        ),
    )
    return markup
