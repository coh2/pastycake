import sys

try:
    from sqlalchemy.orm import sessionmaker

    import sqlalchemy
except ImportError:
    print >> sys.stderr, "This file requires SqlAlchemy."
    raise


from .sql_backend import SqlBackend
from .sql_model import model_base, PasteService, PasteMatcher

print 'foobar'

class SqlAlchemyBackend(SqlBackend):
    def __init__(self, connect_string):
        self._engine = None
        self._session = None
        self._connect_string = connect_string

    def connect(self, *args, **kwargs):
        if not self._engine:
            con_str = args if args else (self._connect_string,)
            self._engine = sqlalchemy.create_engine(*con_str, **kwargs)
            model_base().metadata.create_all(self._engine)
        if not self._session:
            self._session = sessionmaker(bind=self._engine)

    def connected(self):
        return self._engine and self._session

    def already_visited_url(self, url):
        bool(self._session.query(PasteService).filter(url==url).count())

    def save_url(self, url, matches=None):
        #load the matchers
        matchers = []
        for match in matches:
            matchers.append(
                self._session.query(PasteMatcher).filter(matcher==match[0]
                                                        ).one()
            )
        matchers = filter(lambda x: bool(x), matchers)

        #TODO add the matched pieces "somehow"
        match_entry = PasteService(url)
        match_entry.matches += matchers

        self._session.add(match_entry)
        self._session.save()
