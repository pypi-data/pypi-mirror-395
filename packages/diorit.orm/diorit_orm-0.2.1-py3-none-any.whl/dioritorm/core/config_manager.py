import json
import os


class ConfigManager():
    _instance = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, path = 'config.json'):
        if self._config is None:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"Файл {path} не знайдено ⚠")
            with open(path, 'r', encoding='utf-8') as file:
                self._config = json.load(file)
        return self._config

    @property
    def config(self):
        return self._config