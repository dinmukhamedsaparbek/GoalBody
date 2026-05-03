# Goal Body Bot

Telegram бот-нутрициолог. Спрашивает параметры пользователя и выдаёт персональный план питания через Claude AI.

## Требования

- Python 3.10+
- Telegram Bot Token — получить у [@BotFather](https://t.me/BotFather)
- Anthropic API Key — получить на [console.anthropic.com](https://console.anthropic.com)

## Установка

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Запуск

```bash
export TELEGRAM_TOKEN="ваш_токен"
export ANTHROPIC_API_KEY="ваш_ключ"
venv/bin/python bot.py
```

Или через `.env` файл:

```bash
cp .env.example .env
# вписать токены в .env
export $(cat .env | xargs) && venv/bin/python bot.py
```

## Использование

Напиши боту `/start` — он задаст 6 вопросов (вес, рост, возраст, пол, цель, активность) и пришлёт план питания из 4 сообщений.
