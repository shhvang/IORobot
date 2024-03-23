import os
from typing import Dict
import yaml
import functools
from pathlib import Path
from Main import LOGS

lang_strings_cache = {}
languages = {}

@functools.lru_cache(maxsize=None)
def reload_strings(lang_code: str = "en") -> Dict[str, str]:
    lang_file = Path("locales") / f"{lang_code}.yaml"
    if lang_file.exists():
        with lang_file.open("r", encoding="utf-8") as file:
            lang_data = yaml.safe_load(file)
            languages[lang_code] = lang_data  # Store in languages
            return lang_data
    else:
        LOGS.info(f"Localization file not found for '{lang_code}'")
        return {}

def get_string(lang: str, key: str) -> str:
    lang_strings = lang_strings_cache.get(lang)
    if lang_strings is None:
        lang_strings = reload_strings(lang)
        lang_strings_cache[lang] = lang_strings
    return lang_strings.get(key, f"Missing translation for key '{key}'")

def get_languages() -> Dict[str, str]:
    return {lang: data["language"] for lang, data in languages.items()}

def get_language(language: str) -> str:
    return languages[language]["language"]

def setup_localization() -> None:
    lang_files = os.listdir("locales")
    if not lang_files:
        LOGS.info("Localization files not found!")
        LOGS.info("Using the default language - English.")
        reload_strings() 
    else:
        LOGS.info("Localization setup complete!")