from kiyo.logger import logger
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager

class Database:
    def __init__(self, db_uri: str, db_type: str = 'postgresql', debug: bool = False,
                 pool_size: int = 5, max_overflow: int = 10):
        self.metadata = MetaData()
        self.Base = declarative_base(metadata=self.metadata)
        self.Session = None
        self.engine = None
        self.connect(db_uri, db_type, debug, pool_size, max_overflow)
        logger.info("Successfully Connected to SQLAlchemy.")

    def connect(self, db_uri: str, db_type: str, debug: bool,
                pool_size: int, max_overflow: int):
        if db_uri and db_uri.startswith(f"{db_type}://"):
            self.engine = create_engine(db_uri, client_encoding="utf8", echo=debug,
                                        poolclass=QueuePool, pool_size=pool_size,
                                        max_overflow=max_overflow)
        else:
            raise ValueError(f"Invalid database URI or type. Must start with '{db_type}://'.")

        self.metadata.bind = self.engine
        self.Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine, autoflush=False))

    def close(self):
        if self.Session:
            self.Session.close_all()

    def get_session(self):
        return self.Session()

    def get_base(self):
        return self.Base

    def get_engine(self):
        return self.engine

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_all(self):
        """Create all tables in the database."""
        self.Base.metadata.create_all(self.engine)
        logger.info("All tables created.")

    def drop_all(self):
        """Drop all tables in the database."""
        self.Base.metadata.drop_all(self.engine)
        logger.info("All tables dropped.")

    def execute(self, statement):
        """Execute a raw SQL statement."""
        with self.engine.connect() as connection:
            result = connection.execute(statement)
            logger.info("SQL Statement executed.")
            return result

    def __enter__(self):
        return self.get_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
