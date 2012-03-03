'''
the model(s) used by the sqlalchemy backend
'''
import sys

try:
    from sqlalchemy import Column, Integer, String, Table, UnicodeText
    from sqlalchemy import ForeignKey, Sequence
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship
    from sqlalchemy.types import TIMESTAMP
except ImportError:
    print >> sys.stderr, "This file requires SqlAlchemy."
    raise

_Modelbase = declarative_base()


# m:n table has to be non-declarative
paste_match = Table('url_matches', _Modelbase.metadata,
    Column('id', Integer, Sequence('urlmatches_id_seq'),
            primary_key=True, autoincrement=True),
    Column('url', Integer, ForeignKey('urls.id')),
    Column('matcher', Integer, ForeignKey('matchers.id')),
    Column('matched', UnicodeText))


class PasteService(_Modelbase):
    __tablename__ = 'urls'

    id = Column(Integer, Sequence('urls_id_seq'), primary_key=True,
                autoincrement=True)
    url = Column(String)
    viewed = Column(TIMESTAMP)
    pastes = relationship('PasteMatch')

    matches = relationship('PasteMatcher', secondary=paste_match,
                           backref='matched_urls')


class PasteMatcher(_Modelbase):
    __tablename__ = 'matchers'

    id = Column(Integer, Sequence('matchers_id_seq'), primary_key=True,
                autoincrement=True)
    matcher = Column(String)
    #TODO: rel to url_matches


def model_base():
    return _Modelbase
