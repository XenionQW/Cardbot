import threading
import time
import schedule
from database.db import get_connection


def _cleanup_old_history():
    """Удаляем историю старше 30 дней."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM card_history WHERE obtained_at < datetime('now', '-30 days')"
    )
    conn.commit()
    conn.close()


def start_scheduler(bot):
    """Запускает планировщик фоновых задач."""
    schedule.every().day.at("03:00").do(_cleanup_old_history)

    def run():
        while True:
            schedule.run_pending()
            time.sleep(60)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    print("⏰ Планировщик запущен.")
