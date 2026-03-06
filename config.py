import os
from dotenv import load_dotenv

load_dotenv()

# ─── Токен бота ───────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ─── Настройки карточек ───────────────────────────────────────
CARD_COOLDOWN_HOURS = 2          # Кулдаун между открытием карточек
BLACK_HOLE_CHANCE = 0.03         # 3% шанс получить чёрную дыру
LEGENDARY_CHANCE = 0.07          # 7% шанс легендарной
EPIC_CHANCE = 0.15               # 15% шанс эпической
RARE_CHANCE = 0.30               # 30% шанс редкой
# Остаток → обычная (45%)

# ─── Веб-приложение ───────────────────────────────────────────
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8080")  # Замените на свой домен

# ─── Админы ───────────────────────────────────────────────────
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "123456789").split(",")))

# ─── База данных ──────────────────────────────────────────────
DATABASE_PATH = "database/cardbot.db"
