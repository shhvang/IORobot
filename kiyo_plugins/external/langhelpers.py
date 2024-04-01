import os
import yaml
import functools
import logging

from pathlib import Path
from typing import Dict, Union
import sql.language_sql as sql

logs = logging.getLogger(__name__)

lang_strings_cache = {}
languages = {}

@functools.lru_cache(maxsize=None)
def reload_strings(lang_code: str = "en") -> Dict[str, str]:
    lang_file = Path("./kiyo/locales") / f"{lang_code}.yaml"
    if lang_file.exists():
        with lang_file.open("r", encoding="utf-8") as file:
            lang_data = yaml.safe_load(file)
            if lang_data is None or not isinstance(lang_data, dict):
                logs.warning(f"Invalid data format in '{lang_file}' for language '{lang_code}'. Using empty dictionary.")
                lang_data = {}
            languages[lang_code] = lang_data  # Store in languages
            return lang_data
    else:
        logs.info(f"Localization file not found for '{lang_code}'")
        return {}

def get_string(lang: str, key: str) -> str:
    lang_strings = lang_strings_cache.get(lang)
    if lang_strings is None:
        lang_strings = reload_strings(lang)
        lang_strings_cache[lang] = lang_strings
    return lang_strings.get(key, f"Missing translation for key '{key}'")

def get_languages() -> Dict[str, str]:
    return {lang: data.get("language", "") for lang, data in languages.items()}

def get_language(language: str) -> str:
    lang_data = languages.get(language)
    if lang_data:
        return lang_data.get("language", "")
    else:
        return ""

def tlang(
    chat_id: Union[int, str], 
    string: str
) -> str:
    lang = sql.get_chat_lang(chat_id)
    return get_string(lang, string)
