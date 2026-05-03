import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
import anthropic
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
ASK_WEIGHT, ASK_HEIGHT, ASK_AGE, ASK_GENDER, ASK_GOAL, ASK_ACTIVITY = range(6)
GENDER_KEYBOARD   = [["Мужчина", "Женщина"]]
GOAL_KEYBOARD     = [["Набрать мышечную массу", "Похудеть"], ["Поддерживать форму"]]
ACTIVITY_KEYBOARD = [["Сидячий образ жизни", "Лёгкая активность"],
                     ["Умеренная активность", "Высокая активность"]]

def make_keyboard(rows):
    return ReplyKeyboardMarkup(rows, one_time_keyboard=True, resize_keyboard=True)

def valid_options(keyboard):
    return [item for row in keyboard for item in row]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Привет! Я *Goal Body Bot* — твой персональный нутрициолог.\n\n"
        "Отвечу на несколько вопросов и составлю рацион под твои цели.\n\n"
        "Введи свой *вес* (кг), например: `75`",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASK_WEIGHT


async def ask_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(",", ".")
    try:
        val = float(text)
        assert 30 <= val <= 300
    except (ValueError, AssertionError):
        await update.message.reply_text("❗ Введи корректный вес (от 30 до 300 кг):")
        return ASK_WEIGHT
    context.user_data["weight"] = val
    await update.message.reply_text("Введи свой *рост* (см), например: `175`", parse_mode="Markdown")
    return ASK_HEIGHT





