import abc


class KeywordStorage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def enable_keyword(self, kw):
        '''enable the keyword kw.

        If kw isn't one of the available keywords already, it'll be added
        first.

        '''
        pass

    @abc.abstractmethod
    def disable_keyword(self, kw):
        '''disable the keyword kw.

        If kw isn't one of the available keywords already, it'll be added
        first.

        '''
        pass

    @abc.abstractproperty
    def available_keywords(self):
        '''return a list of all known (but perhaps disabled) keywords.'''
        pass

    @abc.abstractproperty
    def current_keywords(self):
        '''return a list of all enabled keywords.'''
        pass

    @property
    def enabled_keywords(self):
        return self.current_keywords
