import logging
import os
from typing import Dict
import yaml
import functools
from pathlib import Path

class Language:
    def __init__(self):
        self.lang_strings_cache = {}
        self.languages = {}
        self.setup_localization()

    def get_string(self, lang: str, key: str) -> str:
        lang_strings = self.lang_strings_cache.get(lang)
        if lang_strings is None:
            lang_strings = self.reload_strings(lang)
            self.lang_strings_cache[lang] = lang_strings
        return lang_strings.get(key, f"Missing translation for key '{key}'")

    @functools.lru_cache(maxsize=None)
    def reload_strings(self, lang_code: str = "en") -> Dict[str, str]:
        lang_file = Path("locales") / f"{lang_code}.yaml"
        if lang_file.exists():
            with lang_file.open("r", encoding="utf-8") as file:
                lang_data = yaml.safe_load(file)
                self.languages[lang_code] = lang_data  # Store in self.languages
                return lang_data
        else:
            logging.info(f"Localization file not found for '{lang_code}'")
            return {}

    def get_languages(self) -> Dict[str, str]:
        return {lang: data["language"] for lang, data in self.languages.items()}

    def get_language(self, language: str) -> str:
        return self.languages[language]["language"]

    def setup_localization(self) -> None:
        lang_files = os.listdir("locales")
        if not lang_files:
            logging.info("Localization files not found!")
            logging.info("Using the default language - English.")
            self.reload_strings() 
        else:
            logging.info("Localization setup complete!")
