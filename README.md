# tz-ai-bot
Telegram бот с ИИ и сохранением контекста диалога

# AI Telegram Bot (Test Task)

Телеграм-бот с интеграцией Gemini 2.0 Flash через OpenRouter.

## Особенности:
- Асинхронность (aiogram 3 + aiohttp).
- Хранение контекста диалога (история сообщений).
- Безопасное хранение ключей в `.env`.

## Как запустить локально:

1. Склонируйте репозиторий.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
3. Создайте файл .env в корневой папке и добавьте свои ключи:
```bash
BOT_TOKEN=ваш_токен_от_BotFather
OPENROUTER_KEY=ваш_ключ_OpenRouter
