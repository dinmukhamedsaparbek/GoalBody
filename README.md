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
## Запуск

```bash
export TELEGRAM_TOKEN="ваш_токен"
export ANTHROPIC_API_KEY="ваш_ключ"
venv/bin/python bot.py
```


```
