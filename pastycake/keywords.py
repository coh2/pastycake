import abc


class KeywordStorage():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def enable_keyword(self, keyword_or_list):
        raise NotImplemented

    @abc.abstractmethod
    def disable_keyword(self, keyword_or_list):
        raise NotImplemented

    @abc.abstractproperty
    def available_keywords(self):
        raise NotImplemented

    @abc.abstractproperty
    def current_keywords(self):
        raise NotImplemented
