import aiogram
from dispathcher import dp
import handlers
from db import BotDB
BotDB = BotDB('accountant.db')
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
