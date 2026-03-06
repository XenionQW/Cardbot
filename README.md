# 🌌 CardBlackHole — Telegram Card Bot

Карточный бот с космической тематикой, чёрными дырами и Telegram WebApp.

## 🚀 Запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка

```bash
cp .env.example .env
# Открой .env и заполни BOT_TOKEN, ADMIN_IDS, WEBAPP_URL
```

### 3. Запуск

```bash
python bot.py
```

---

## 📁 Структура проекта

```
cardbot/
├── bot.py                  # Точка входа
├── config.py               # Конфигурация
├── requirements.txt
├── .env.example
│
├── database/
│   └── db.py               # SQLite: инициализация, запросы
│
├── handlers/
│   ├── start.py            # /start, /help, /menu
│   ├── cards.py            # Открытие карточек
│   ├── collection.py       # Коллекция, топ игроков
│   └── admin.py            # Панель администратора
│
├── keyboards/
│   └── keyboards.py        # Клавиатуры и кнопки
│
├── utils/
│   ├── card_logic.py       # Логика карточек, редкости, кулдаун
│   └── scheduler.py        # Фоновые задачи
│
└── webapp/
    ├── server.py           # Flask веб-сервер
    └── templates/
        ├── index.html
        └── collection.html # WebApp коллекции
```

---

## 🃏 Система редкостей

| Редкость     | Шанс | Цвет  |
|--------------|------|-------|
| ⬜ Обычная   | 45%  | Серый |
| 🔵 Редкая    | 30%  | Синий |
| 🟣 Эпическая | 15%  | Фиолетовый |
| 🟡 Легендарная | 7% | Золотой |
| 🕳️ Чёрная дыра | 3% | Чёрный |

## ⏱ Кулдаун

Одну карточку можно открыть раз в **2 часа** (настраивается в `config.py`).

## 🌐 WebApp

Коллекция открывается в Telegram Mini App с красивым интерфейсом.  
Для работы нужен публичный HTTPS-домен (можно использовать [ngrok](https://ngrok.com) для тестирования).

```bash
ngrok http 8080
# Полученный URL вставь в WEBAPP_URL в .env
```

## 🔧 Команды администратора

- `/admin` — панель
- `/stats` — статистика
- `/cards` — список карточек
- `/addcard` — добавить карточку
