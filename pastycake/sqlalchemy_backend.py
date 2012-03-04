import sys

try:
    from sqlalchemy.orm import sessionmaker

    import sqlalchemy
except ImportError:
    print >> sys.stderr, "This file requires SqlAlchemy."
    raise


from .sql_backend import SqlBackend
from .sql_model import model_base


class SqlAlchemyBackend(SqlBackend):
    def __init__(self):
        self._engine = None
        self._session = None

    def connect(self, *args, **kwargs):
        if not self._engine:
            self._engine = sqlalchemy.create_engine(*args, **kwargs)
            model_base().metadata.create_all(self._engine)
        if not self._session:
            self._session = sessionmaker(bind=self._engine)

    def connected(self):
        return self._engine and self._session

    def _session(self):
        return self._session()
