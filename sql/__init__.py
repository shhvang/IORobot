from kiyo.lib.database import Database
from kiyo import configs as config

database = Database(
    config.DATABASE_URI, db_type='postgresql', pool_size=10, max_overflow=20, debug=False
)
