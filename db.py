import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация базы данных и создание таблиц."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            first_name  TEXT,
            last_name   TEXT,
            registered_at TEXT DEFAULT (datetime('now')),
            last_card_at  TEXT DEFAULT NULL,
            total_cards   INTEGER DEFAULT 0,
            black_holes   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS cards (
            card_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            rarity      TEXT NOT NULL,  -- common, rare, epic, legendary, black_hole
            power       INTEGER DEFAULT 0,
            image_url   TEXT,
            emoji       TEXT DEFAULT '🃏'
        );

        CREATE TABLE IF NOT EXISTS user_cards (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            card_id     INTEGER NOT NULL,
            obtained_at TEXT DEFAULT (datetime('now')),
            count       INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (card_id) REFERENCES cards(card_id)
        );

        CREATE TABLE IF NOT EXISTS card_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            card_id     INTEGER NOT NULL,
            obtained_at TEXT DEFAULT (datetime('now'))
        );
    """)

    conn.commit()
    _seed_cards(cursor, conn)
    conn.close()
    print("✅ База данных инициализирована.")


def _seed_cards(cursor, conn):
    """Заполнение таблицы карточками по умолчанию."""
    cursor.execute("SELECT COUNT(*) FROM cards")
    if cursor.fetchone()[0] > 0:
        return  # уже заполнено

    cards = [
        # ── Обычные ──────────────────────────────────────────────
        ("Звёздная пыль",   "Остатки умершей звезды.",                "common",     10, "✨"),
        ("Метеорит",        "Камень из глубин космоса.",              "common",     15, "🪨"),
        ("Комета",          "Ледяной странник с хвостом из света.",   "common",     20, "☄️"),
        ("Спутник",         "Верный страж планеты.",                  "common",     25, "🛰️"),
        ("Астероид",        "Угроза из пояса астероидов.",            "common",     30, "🌑"),

        # ── Редкие ───────────────────────────────────────────────
        ("Красный гигант",  "Умирающая звезда колоссальных размеров.","rare",       50, "🔴"),
        ("Туманность",      "Колыбель новых звёзд.",                  "rare",       60, "🌌"),
        ("Пульсар",         "Вращающийся маяк вселенной.",            "rare",       70, "💫"),
        ("Квазар",          "Самый яркий объект во вселенной.",       "rare",       80, "🌠"),

        # ── Эпические ────────────────────────────────────────────
        ("Нейтронная звезда","Сверхплотный остаток взрыва.",          "epic",      120, "⚡"),
        ("Сверхновая",      "Взрыв звезды, видимый за миллиарды лет.","epic",      150, "💥"),
        ("Тёмная материя",  "Невидимая основа вселенной.",            "epic",      180, "🌫️"),
        ("Антиматерия",     "Зеркальное отражение реальности.",       "epic",      200, "⚗️"),

        # ── Легендарные ───────────────────────────────────────────
        ("Галактика",       "Миллиарды звёзд в одном объекте.",       "legendary", 350, "🌀"),
        ("Вселенная",       "Всё, что существует.",                   "legendary", 500, "🔭"),
        ("Большой взрыв",   "Начало всего.",                          "legendary", 777, "🎆"),

        # ── Чёрные дыры ──────────────────────────────────────────
        ("Чёрная дыра I",   "Маленький монстр, пожирающий свет.",     "black_hole", 999, "🕳️"),
        ("Чёрная дыра II",  "Сверхмассивный пожиратель галактик.",    "black_hole",1500, "⚫"),
        ("Сингулярность",   "Точка, где законы физики рушатся.",      "black_hole",9999, "🌑"),
    ]

    cursor.executemany(
        "INSERT INTO cards (name, description, rarity, power, emoji) VALUES (?,?,?,?,?)",
        cards
    )
    conn.commit()
    print(f"🃏 Добавлено {len(cards)} карточек в базу.")


# ─── Пользователи ─────────────────────────────────────────────

def get_or_create_user(user_id: int, username: str, first_name: str, last_name: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name, last_name) VALUES (?,?,?,?)",
            (user_id, username, first_name, last_name)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
    conn.close()
    return dict(user)


def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def update_last_card_time(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_card_at = datetime('now'), total_cards = total_cards + 1 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()


def increment_black_holes(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET black_holes = black_holes + 1 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()


# ─── Карточки ────────────────────────────────────────────────

def get_random_card(rarity: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cards WHERE rarity = ? ORDER BY RANDOM() LIMIT 1",
        (rarity,)
    )
    card = cursor.fetchone()
    conn.close()
    return dict(card) if card else None


def add_card_to_user(user_id: int, card_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, count FROM user_cards WHERE user_id = ? AND card_id = ?",
        (user_id, card_id)
    )
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            "UPDATE user_cards SET count = count + 1 WHERE id = ?",
            (existing["id"],)
        )
    else:
        cursor.execute(
            "INSERT INTO user_cards (user_id, card_id) VALUES (?,?)",
            (user_id, card_id)
        )
    cursor.execute(
        "INSERT INTO card_history (user_id, card_id) VALUES (?,?)",
        (user_id, card_id)
    )
    conn.commit()
    conn.close()


def get_user_collection(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, uc.count, uc.obtained_at
        FROM user_cards uc
        JOIN cards c ON c.card_id = uc.card_id
        WHERE uc.user_id = ?
        ORDER BY c.rarity DESC, c.power DESC
    """, (user_id,))
    cards = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cards


def get_top_users(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.user_id, u.first_name, u.username, u.total_cards, u.black_holes,
               COALESCE(SUM(c.power * uc.count), 0) as total_power
        FROM users u
        LEFT JOIN user_cards uc ON uc.user_id = u.user_id
        LEFT JOIN cards c ON c.card_id = uc.card_id
        GROUP BY u.user_id
        ORDER BY total_power DESC
        LIMIT ?
    """, (limit,))
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


def get_all_cards():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards ORDER BY rarity, power")
    cards = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cards
