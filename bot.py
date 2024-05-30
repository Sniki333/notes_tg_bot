import telebot
import os
from dotenv import load_dotenv
from database import DB

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
])


@bot.message_handler(commands=["start"])
def start_command(message: telebot.types.Message):
    bot.send_message(message.from_user.id, "Привет")
    db = DB()
    if not db.telegram_user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
