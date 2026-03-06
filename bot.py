import telebot
import threading
from config import BOT_TOKEN
from database.db import init_db
from handlers.start import register_start_handlers
from handlers.cards import register_card_handlers
from handlers.collection import register_collection_handlers
from handlers.admin import register_admin_handlers
from utils.scheduler import start_scheduler
from webapp.server import start_webapp

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


def main():
    print("🚀 Запуск бота...")
    init_db()
    register_start_handlers(bot)
    register_card_handlers(bot)
    register_collection_handlers(bot)
    register_admin_handlers(bot)
    start_scheduler(bot)

    # Запуск веб-приложения в отдельном потоке
    webapp_thread = threading.Thread(target=start_webapp, daemon=True)
    webapp_thread.start()

    print("✅ Бот запущен!")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)


if __name__ == "__main__":
    main()
