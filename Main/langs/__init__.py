from typing import Union
import Main.sql.language_sql as sql
from Main.langs.helpers import (
    get_language,
    get_languages,
    get_string,
    setup_localization
)

def tlang(
    chat_id: Union[int, str], 
    string: str
) -> str:
    lang = sql.get_chat_lang(chat_id)
    return get_string(lang, string)

def useless_func() -> str:
    return tlang, get_string