import random
from datetime import datetime, timedelta
from config import (
    CARD_COOLDOWN_HOURS, BLACK_HOLE_CHANCE,
    LEGENDARY_CHANCE, EPIC_CHANCE, RARE_CHANCE
)
from database.db import (
    get_user, update_last_card_time, get_random_card,
    add_card_to_user, increment_black_holes
)

RARITY_LABELS = {
    "common":     "⬜ Обычная",
    "rare":       "🔵 Редкая",
    "epic":       "🟣 Эпическая",
    "legendary":  "🟡 Легендарная",
    "black_hole": "🕳️ Чёрная дыра",
}

RARITY_COLORS = {
    "common":     "#9e9e9e",
    "rare":       "#2196f3",
    "epic":       "#9c27b0",
    "legendary":  "#ffc107",
    "black_hole": "#000000",
}


def get_cooldown_remaining(user: dict) -> timedelta | None:
    """Возвращает оставшееся время кулдауна или None если кулдаун прошёл."""
    if not user.get("last_card_at"):
        return None
    last = datetime.strptime(user["last_card_at"], "%Y-%m-%d %H:%M:%S")
    next_card = last + timedelta(hours=CARD_COOLDOWN_HOURS)
    now = datetime.utcnow()
    if now >= next_card:
        return None
    return next_card - now


def format_cooldown(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def roll_rarity() -> str:
    """Определяет редкость случайной карточки."""
    r = random.random()
    if r < BLACK_HOLE_CHANCE:
        return "black_hole"
    r -= BLACK_HOLE_CHANCE
    if r < LEGENDARY_CHANCE:
        return "legendary"
    r -= LEGENDARY_CHANCE
    if r < EPIC_CHANCE:
        return "epic"
    r -= EPIC_CHANCE
    if r < RARE_CHANCE:
        return "rare"
    return "common"


def open_card(user_id: int) -> dict | None:
    """
    Пытается открыть карточку для пользователя.
    Возвращает словарь с карточкой или None если кулдаун не прошёл.
    """
    user = get_user(user_id)
    if not user:
        return None

    cooldown = get_cooldown_remaining(user)
    if cooldown:
        return {"cooldown": format_cooldown(cooldown)}

    rarity = roll_rarity()
    card = get_random_card(rarity)
    if not card:
        # Фолбэк на обычную если редкость не найдена
        card = get_random_card("common")

    add_card_to_user(user_id, card["card_id"])
    update_last_card_time(user_id)

    if rarity == "black_hole":
        increment_black_holes(user_id)

    return {"card": card, "rarity_label": RARITY_LABELS[rarity]}


def build_card_message(card: dict, rarity_label: str) -> str:
    """Формирует красивое сообщение с карточкой."""
    emoji = card.get("emoji", "🃏")
    name = card["name"]
    desc = card["description"]
    power = card["power"]
    rarity = card["rarity"]

    if rarity == "black_hole":
        header = "🌑✨ <b>ЧЁРНАЯ ДЫРА!</b> ✨🌑\n<i>Невероятная удача!</i>"
    elif rarity == "legendary":
        header = "🌟 <b>ЛЕГЕНДАРНАЯ КАРТОЧКА!</b> 🌟"
    elif rarity == "epic":
        header = "💜 <b>Эпическая карточка!</b> 💜"
    elif rarity == "rare":
        header = "💙 <b>Редкая карточка!</b> 💙"
    else:
        header = "🃏 <b>Карточка получена!</b>"

    return (
        f"{header}\n\n"
        f"{emoji} <b>{name}</b>\n"
        f"├ Редкость: {rarity_label}\n"
        f"├ Сила: ⚡ {power}\n"
        f"└ <i>{desc}</i>"
    )
