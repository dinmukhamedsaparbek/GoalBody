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
    async def ask_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(",", ".")
    try:
        val = float(text)
        assert 100 <= val <= 250
    except (ValueError, AssertionError):
        await update.message.reply_text("❗ Введи корректный рост (от 100 до 250 см):")
        return ASK_HEIGHT
    context.user_data["height"] = val
    await update.message.reply_text("Введи свой *возраст* (лет), например: `25`", parse_mode="Markdown")
    return ASK_AGE


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        val = int(update.message.text.strip())
        assert 10 <= val <= 100
    except (ValueError, AssertionError):
        await update.message.reply_text("❗ Введи корректный возраст (от 10 до 100):")
        return ASK_AGE
    context.user_data["age"] = val
    await update.message.reply_text("Укажи свой пол:", reply_markup=make_keyboard(GENDER_KEYBOARD))
    return ASK_GENDER


async def save_button_value(update, context, keyboard, key):
    """Validates the user's button choice. Returns the value on success, None to show the keyboard again."""
    value = update.message.text.strip()
    if value not in valid_options(keyboard):
        await update.message.reply_text("❗ Выбери из предложенных вариантов:", reply_markup=make_keyboard(keyboard))
        return None
    context.user_data[key] = value
    return value
    async def ask_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await save_button_value(update, context, GENDER_KEYBOARD, "gender"):
        return ASK_GENDER
    await update.message.reply_text("🎯 Какова твоя цель?", reply_markup=make_keyboard(GOAL_KEYBOARD))
    return ASK_GOAL


async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await save_button_value(update, context, GOAL_KEYBOARD, "goal"):
        return ASK_GOAL
    await update.message.reply_text("🏃 Уровень физической активности?", reply_markup=make_keyboard(ACTIVITY_KEYBOARD))
    return ASK_ACTIVITY


async def ask_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Final step: calls the AI and delivers the plan split into 4 separate messages via SPLIT."""
    if not await save_button_value(update, context, ACTIVITY_KEYBOARD, "activity"):
        return ASK_ACTIVITY


    await update.message.reply_text("⏳ Составляю план питания...", reply_markup=ReplyKeyboardRemove())

    d = context.user_data
    prompt = (
        f"Ты — профессиональный нутрициолог и фитнес-тренер. Данные пользователя:\n"
        f"Пол: {d['gender']}, возраст: {d['age']} лет, вес: {d['weight']} кг, рост: {d['height']} см.\n"
        f"Цель: {d['goal']}. Активность: {d['activity']}.\n\n"
        f"Составь персональный план питания, разбив ответ ровно на 4 блока.\n"
        f"Между каждым блоком поставь разделитель: |||SPLIT|||\n\n"
        f"Блок 1: Суточная норма калорий (формула Миффлина-Сан Жеора + активность + цель).\n"
        f"Блок 2: БЖУ в граммах и процентах.\n"
        f"Блок 3: Меню на 1 день (завтрак, обед, ужин, 2 перекуса) с граммовкой и калориями.\n"
        f"Блок 4: 3–5 рекомендаций под цель.\n\n"
        f"Отвечай чётко, на русском. Используй эмодзи. "
        f"Не используй markdown-разметку (никаких *, **, #, _ и т.п.) — только обычный текст."
    )







