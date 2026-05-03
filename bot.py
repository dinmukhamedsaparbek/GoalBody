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
