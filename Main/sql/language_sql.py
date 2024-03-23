import threading
from sqlalchemy import Column, String, UnicodeText
from Main.sql import Session, Base


class ChatLangs(Base):
    __tablename__ = "chatlangs"
    chat_id = Column(String(14), primary_key=True)
    language = Column(UnicodeText)

    def __init__(self, chat_id, language):
        self.chat_id = str(chat_id)  
        self.language = language

    def __repr__(self):
        return f"<ChatLangs(chat_id='{self.chat_id}', language='{self.language}')>"

Base.metadata.create_all(bind=Session.get_bind(), checkfirst=True)

CHAT_LANG = {}
LANG_LOCK = threading.RLock()


def set_lang(chat_id: str, lang: str) -> None:
    with LANG_LOCK:
        curr = Session.query(ChatLangs).get(str(chat_id))
        if not curr:
            curr = ChatLangs(str(chat_id), lang)
            Session.add(curr)
            Session.flush()
        else:
            curr.language = lang

        CHAT_LANG[str(chat_id)] = lang
        Session.commit()


def get_chat_lang(chat_id: str) -> str:
    lang = CHAT_LANG.get(str(chat_id))
    if lang is None:
        lang = "en"
    return lang


def __load_chat_language() -> None:
    global CHAT_LANG
    try:
        allchats = Session.query(ChatLangs).all()
        CHAT_LANG = {x.chat_id: x.language for x in allchats}
    finally:
        Session.close()


__load_chat_language()
