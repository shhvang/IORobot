from IO.lib.database import Database
from IO import configs as config

database = Database(
    config.DATABASE_URI, db_type='postgresql', pool_size=10, max_overflow=20, debug=False
)
Session = database.get_session()
Engine = database.get_engine()
Base = database.get_base()
