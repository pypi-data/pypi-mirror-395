import sqlite3
import os
from .databasehandler import DatabaseHandler
from dioritorm.core.constants import DATABASE_PATH

class SQLiteHandler(DatabaseHandler):  # Було `SQLiteGandler`, виправив
    def __init__(self):
        super().__init__()

        # Переконуємося, що директорія існує
        if not os.path.exists(DATABASE_PATH):
            os.makedirs(DATABASE_PATH)

        # Створюємо шлях до бази коректним способом
        db_path = os.path.join(DATABASE_PATH, "data.db")

        # Підключаємося до SQLite
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def save(self, json_data):
        pass  # Тут буде логіка збереження

    def close(self):
        """Закриває підключення до бази"""
        if self.connection:
            self.connection.close()
