from telebot import TeleBot
from telebot.types import Message
from config import ADMIN_IDS
from database.db import get_connection, get_all_cards


def register_admin_handlers(bot: TeleBot):

    def is_admin(user_id: int) -> bool:
        return user_id in ADMIN_IDS

    @bot.message_handler(commands=["admin"])
    def cmd_admin(message: Message):
        if not is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "❌ Нет доступа.")
            return
        bot.send_message(
            message.chat.id,
            "🔧 <b>Панель администратора</b>\n\n"
            "/stats — статистика бота\n"
            "/cards — список всех карточек\n"
            "/addcard — добавить карточку (формат ниже)\n"
        )

    @bot.message_handler(commands=["stats"])
    def cmd_stats(message: Message):
        if not is_admin(message.from_user.id):
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        users = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM card_history")
        opens = cursor.fetchone()["cnt"]
        cursor.execute("SELECT COUNT(*) as cnt FROM card_history WHERE card_id IN (SELECT card_id FROM cards WHERE rarity='black_hole')")
        bh = cursor.fetchone()["cnt"]
        conn.close()
        bot.send_message(
            message.chat.id,
            f"📊 <b>Статистика:</b>\n"
            f"👥 Пользователей: {users}\n"
            f"🃏 Всего открыто карточек: {opens}\n"
            f"🕳️ Чёрных дыр выпало: {bh}"
        )

    @bot.message_handler(commands=["cards"])
    def cmd_cards(message: Message):
        if not is_admin(message.from_user.id):
            return
        cards = get_all_cards()
        lines = [f"🃏 <b>Все карточки ({len(cards)}):</b>\n"]
        for c in cards:
            lines.append(f"{c['emoji']} [{c['rarity']}] {c['name']} — ⚡{c['power']}")
        bot.send_message(message.chat.id, "\n".join(lines))

    @bot.message_handler(commands=["addcard"])
    def cmd_addcard(message: Message):
        if not is_admin(message.from_user.id):
            return
        bot.send_message(
            message.chat.id,
            "📝 Отправь данные карточки в формате:\n\n"
            "<code>name|description|rarity|power|emoji</code>\n\n"
            "Пример:\n"
            "<code>Гиперновая|Взрыв сверхновой в кубе|epic|250|🌟</code>\n\n"
            "Редкости: common, rare, epic, legendary, black_hole"
        )
        bot.register_next_step_handler(message, _process_addcard)

    def _process_addcard(message: Message):
        if not is_admin(message.from_user.id):
            return
        try:
            parts = message.text.strip().split("|")
            name, desc, rarity, power, emoji = [p.strip() for p in parts]
            valid_rarities = {"common", "rare", "epic", "legendary", "black_hole"}
            if rarity not in valid_rarities:
                bot.send_message(message.chat.id, f"❌ Неверная редкость: {rarity}")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cards (name, description, rarity, power, emoji) VALUES (?,?,?,?,?)",
                (name, desc, rarity, int(power), emoji)
            )
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, f"✅ Карточка <b>{name}</b> добавлена!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка: {e}\n\nПроверь формат.")
