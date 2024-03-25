import threading
from sqlalchemy import Column, String, UnicodeText, distinct, func
from . import Base, Session

class Rules(Base):
    __tablename__ = "rules"
    chat_id = Column(String(14), primary_key=True)
    rules = Column(UnicodeText, default="")

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return "<Chat {} rules: {}>".format(self.chat_id, self.rules)

Base.metadata.create_all(bind=Session.get_bind(), checkfirst=True)

INSERTION_LOCK = threading.RLock()

def set_rules(chat_id, rules_text):
    with INSERTION_LOCK:
        rules = Session.query(Rules).get(str(chat_id))
        if not rules:
            rules = Rules(str(chat_id))
        rules.rules = rules_text

        session = Session
        session.add(rules)
        session.commit()
        session.close()

def get_rules(chat_id):
    session = Session
    rules = session.query(Rules).get(str(chat_id))
    ret = ""
    if rules:
        ret = rules.rules
    session.close()
    return ret

def num_chats():
    try:
        session = Session
        return session.query(func.count(distinct(Rules.chat_id))).scalar()
    finally:
        session.close()

def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        session = Session
        chat = session.query(Rules).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        session.commit()
        session.close()
