from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from database.db import get_or_create_user
from utils.card_logic import open_card, build_card_message
from keyboards.keyboards import open_card_keyboard, after_card_keyboard, main_menu_keyboard


def register_card_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text == "🃏 Открыть карточку")
    def msg_open_card(message: Message):
        _process_open_card(bot, message.chat.id, message.from_user.id, message.from_user)

    @bot.callback_query_handler(func=lambda c: c.data == "open_card")
    def cb_open_card(call: CallbackQuery):
        bot.answer_callback_query(call.id)
        _process_open_card(bot, call.message.chat.id, call.from_user.id, call.from_user)

    @bot.message_handler(func=lambda m: m.text == "ℹ️ О боте")
    def msg_about(message: Message):
        text = (
            "🌌 <b>CardBlackHole</b>\n\n"
            "<b>Редкости карточек:</b>\n"
            "⬜ Обычная — 45%\n"
            "🔵 Редкая — 30%\n"
            "🟣 Эпическая — 15%\n"
            "🟡 Легендарная — 7%\n"
            "🕳️ Чёрная дыра — 3%\n\n"
            "⏱ Кулдаун: 2 часа между открытиями\n"
            "📦 Дубликаты карточек засчитываются в коллекцию\n"
            "🏆 Рейтинг считается по суммарной силе карточек"
        )
        bot.send_message(message.chat.id, text)


def _process_open_card(bot: TeleBot, chat_id: int, user_id: int, user_obj):
    get_or_create_user(
        user_id=user_obj.id,
        username=user_obj.username or "",
        first_name=user_obj.first_name or "",
        last_name=user_obj.last_name or "",
    )

    result = open_card(user_id)

    if not result:
        bot.send_message(chat_id, "❌ Произошла ошибка. Попробуйте ещё раз.")
        return

    if "cooldown" in result:
        remaining = result["cooldown"]
        bot.send_message(
            chat_id,
            f"⏳ <b>Кулдаун!</b>\n\n"
            f"Следующую карточку можно открыть через:\n"
            f"<code>{remaining}</code>\n\n"
            f"Возвращайся позже! 🌌",
            reply_markup=open_card_keyboard()
        )
        return

    card = result["card"]
    rarity_label = result["rarity_label"]
    text = build_card_message(card, rarity_label)

    bot.send_message(
        chat_id,
        text,
        reply_markup=after_card_keyboard(user_id)
    )
