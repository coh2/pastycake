import sys

try:
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.exc import NoResultFound

    import sqlalchemy
except ImportError:
    print >> sys.stderr, "This file requires SqlAlchemy."
    raise

from .sql_backend import SqlBackend
from .sql_model import model_base, PasteService, PasteMatcher


class SqlAlchemyBackend(SqlBackend):
    def __init__(self, connect_string=None):
        self._engine = None
        self._sessionobj = None
        self._sessioninst = None
        self._connect_string = connect_string

    def connect(self, *args, **kwargs):
        if not self._engine:
            con_str = args if args else (self._connect_string,)
            self._engine = sqlalchemy.create_engine(*con_str, **kwargs)
            model_base().metadata.create_all(self._engine)
        if not self._sessionobj:
            self._sessionobj = sessionmaker(bind=self._engine)

    def connected(self):
        return self._engine and self._session

    def _session(self):
        if not self._sessioninst:
            self._sessioninst = self._sessionobj()
        return self._sessioninst

    def already_visited_url(self, url):
        if not self.connected():
            self.connect()
        bool(self._session().query(PasteService).filter(PasteService.url==url).count())

    def save_url(self, url, matches=None):
        #load the matchers
        matchers = []

        if matches:
            for match in matches:
                try:
                    matchers.append(
                        self._session().query(PasteMatcher).filter(
                            PasteMatcher.matcher==match[0]
                        ).one()
                    )
                except NoResultFound:
                    continue
        matchers = filter(lambda x: bool(x), matchers)

        #TODO add the matched pieces "somehow"
        match_entry = PasteService(url)
        match_entry.matches += matchers

        self._session().add(match_entry)
        self._session().commit()
