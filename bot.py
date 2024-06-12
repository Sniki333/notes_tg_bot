import telebot
from telebot import types


class NotesBot:
    def __init__(self, TOKEN, db):
        self.bot = telebot.TeleBot(TOKEN)
        self.bot.set_my_commands([
            telebot.types.BotCommand("/start", "register"),
            telebot.types.BotCommand("/add", "add a note"),
            telebot.types.BotCommand("/notes", "notes list"),
            telebot.types.BotCommand("/delete", "delete your note"),
        ])
        self.set_handlers()

        self.db = db

    def run(self):
        self.bot.polling()

    def set_handlers(self):
        @self.bot.message_handler(commands=["start"])
        def start_command(message: telebot.types.Message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Information")
            markup.add(btn1)
            self.bot.send_message(message.from_user.id, "Нажмите кнопку 'Information' чтобы получить справку",
                                  reply_markup=markup)
            if not self.db.telegram_user_exists(message.from_user.id):
                self.db.add_user(message.from_user.id, message.from_user.username)
                self.bot.send_message(message.from_user.id, "hello")
            else:
                self.bot.send_message(message.from_user.id, "Добро пожаловать обратно!")

            self.bot.send_message(message.from_user.id,
                                  "Используйте команду `/add <текст заметки>` для добавления заметки.")

        @self.bot.message_handler(commands=['add'])
        def add_note_handler(message):
            note_text = message.text[len('/add '):]
            if len(note_text) == 0:
                self.bot.reply_to(message, "Используйте команду `/add <текст заметки>` для добавления заметки.")
                return

            user_id = self.db.get_user_id(message.from_user.id)
            self.db.add_note(user_id, note_text)
            self.bot.reply_to(message, "Заметка сохранена!")

        @self.bot.message_handler(commands=['notes'])
        def list_notes_handler(message):
            notes = self.db.get_notes(message.from_user.id)
            if notes:
                response = "Ваши заметки:\n" + "\n".join([f"{note[0]}. {note[1]}" for note in notes])
            else:
                response = "У вас нет сохранённых заметок."
            self.bot.reply_to(message, response)

        @self.bot.message_handler(commands=['delete'])
        def delete_note_handler(message):
            note_id = message.text[len('/delete '):]
            if len(note_id) == 0:
                self.bot.reply_to(message, "Используйте команду `/delete <номер заметки>` для удаления заметки.")
                return
            user_id = message.from_user.id
            self.db.delete_note(user_id, note_id)
            self.bot.reply_to(message, "Заметка удалена!")

        @self.bot.message_handler(content_types=["text"])
        def func(message):
            if message.text == "Information":
                self.bot.send_message(message.chat.id, text="Этот бот создан для создания и хранения заметок.\n" +
                                                            "/start - запуск\n" +
                                                            "/add {text}\n" +
                                                            "/notes - показать заметки\n" +
                                                            "/delete {num} - удаление заметки")

        @self.bot.message_handler(content_types=["photo"])
        def func_photo_handler(message):
            self.bot.send_message(message.chat.id, "красивое фото")

        @self.bot.message_handler(content_types=["video"])
        def func_photo_handler(message):
            self.bot.send_message(message.chat.id, "классное видео")

        @self.bot.message_handler(content_types=["sticker"])
        def func_photo_handler(message):
            self.bot.send_message(message.chat.id, "классный стикер")
