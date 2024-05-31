import os
from bot import NotesBot
from dotenv import load_dotenv
from database import DB

load_dotenv()


def main():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    db = DB('database.sqlite')

    notes_bot = NotesBot(TOKEN, db)
    notes_bot.run()


if __name__ == "__main__":
    main()
