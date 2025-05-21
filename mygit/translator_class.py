import json
from pathlib import Path

class Translator :
    def __init__(self, filepath: str, default_lang: str = "ru"):
        self.filepath = Path(filepath)
        self.default_lang = default_lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        with open(self.filepath, "r", encoding="utf-8") as file:
            self.translations = json.load(file)


    def set_language(self, lang: str):
        if lang in self.translations:
            self.default_lang = lang
            print(self.default_lang)
        else:
            raise ValueError(f"Language '{lang}' not found in translation file")


    def t(self, key: str, lang: str = None) -> str|None:
        lang = lang or self.default_lang
        text = self.translations.get(lang, {}).get(key, key)
        if text is None :
            return key
        return self.translations.get(lang, {}).get(key, key)