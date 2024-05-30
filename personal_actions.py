from aiogram import types
from dis
import config
import re
from bot import BotDB

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать")


@dp.message_handler(commands=['create personage'])
async def start(message: types.Message):
    [type_personage, name] = message.text.split(",")
    BotDB.add_personage(message.from_user.id, type_personage, name)

    
    kb = types.KeyboardButton(text="Выберите класс персонажа")
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.bot.send_message(message.from_user.id, "Выберите класс персонажа", reply_markup=keyboard)

@dp.message_handler(commands=['Выберите класс персонажа'])
async def choose_class(message: types.Message):
     kb = [
        [types.KeyboardButton(text="Человек")],
        [types.KeyboardButton(text="Кот")],
        [types.KeyboardButton(text="Собака")],
        [types.KeyboardButton(text="Неопознанный")]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.bot.send_message("Выберите класс персонажа", reply_markup=keyboard)


@dp.message_handler(commands=["text"])
async def text(message: types.Message):
    if text == "Человек":
