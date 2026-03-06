from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from database.db import get_user_collection, get_user, get_top_users
from keyboards.keyboards import collection_keyboard, main_menu_keyboard
from utils.card_logic import RARITY_LABELS


def register_collection_handlers(bot: TeleBot):

    @bot.message_handler(func=lambda m: m.text == "📦 Моя коллекция")
    def msg_collection(message: Message):
        _send_collection(bot, message.chat.id, message.from_user.id)

    @bot.callback_query_handler(func=lambda c: c.data == "my_collection")
    def cb_collection(call: CallbackQuery):
        bot.answer_callback_query(call.id)
        _send_collection(bot, call.message.chat.id, call.from_user.id)

    @bot.message_handler(func=lambda m: m.text == "🏆 Топ игроков")
    def msg_top(message: Message):
        top = get_top_users(10)
        if not top:
            bot.send_message(message.chat.id, "😶 Пока никого нет в рейтинге.")
            return

        lines = ["🏆 <b>Топ игроков по силе коллекции:</b>\n"]
        medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 10

        for i, u in enumerate(top):
            name = u["first_name"] or u["username"] or f"User{u['user_id']}"
            lines.append(
                f"{medals[i]} <b>{name}</b>\n"
                f"   ⚡ Сила: {u['total_power']} | 🃏 Карточек: {u['total_cards']} | 🕳️ ЧД: {u['black_holes']}"
            )

        bot.send_message(message.chat.id, "\n".join(lines))


def _send_collection(bot: TeleBot, chat_id: int, user_id: int):
    user = get_user(user_id)
    cards = get_user_collection(user_id)

    if not cards:
        bot.send_message(
            chat_id,
            "📦 <b>Твоя коллекция пуста!</b>\n\nНажми '🃏 Открыть карточку' чтобы начать."
        )
        return

    total_power = sum(c["power"] * c["count"] for c in cards)
    unique = len(cards)
    total = sum(c["count"] for c in cards)

    # Группируем по редкости
    by_rarity = {}
    for card in cards:
        r = card["rarity"]
        by_rarity.setdefault(r, []).append(card)

    order = ["black_hole", "legendary", "epic", "rare", "common"]
    lines = [
        f"📦 <b>Коллекция</b>\n",
        f"🃏 Карточек: {total} ({unique} уникальных)",
        f"⚡ Суммарная сила: {total_power}",
        f"🕳️ Чёрных дыр: {user.get('black_holes', 0)}\n",
    ]

    for rarity in order:
        if rarity not in by_rarity:
            continue
        label = RARITY_LABELS[rarity]
        lines.append(f"\n<b>{label}:</b>")
        for c in by_rarity[rarity]:
            count_str = f" ×{c['count']}" if c["count"] > 1 else ""
            lines.append(f"  {c['emoji']} {c['name']}{count_str} (⚡{c['power']})")

    bot.send_message(
        chat_id,
        "\n".join(lines),
        reply_markup=collection_keyboard(user_id)
    )
