import threading

from Main.sql import Base, Session
from sqlalchemy import Column, String, UnicodeText

class Rules(Base):
    __tablename__ = "rules"
    chat_id = Column(String(14), primary_key=True)
    rules = Column(UnicodeText, default="")

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return "<Chat {} rules: {}>".format(self.chat_id, self.rules)


Rules.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def set_rules(chat_id, rules_text):
    with INSERTION_LOCK:
        rules = Session.query(Rules).get(str(chat_id))
        if not rules:
            rules = Rules(str(chat_id))
        rules.rules = rules_text

        Session.add(rules)
        Session.commit()


def get_rules(chat_id):
    rules = Session.query(Rules).get(str(chat_id))
    ret = ""
    if rules:
        ret = rules.rules

    Session.close()
    return ret


def num_chats():
    try:
        return Session.query(func.count(distinct(Rules.chat_id))).scalar()
    finally:
        Session.close()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = Session.query(Rules).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        Session.commit()