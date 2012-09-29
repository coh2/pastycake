import abc


class StorageBackend:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def already_visited_url(self, url):
        '''
        @return True if the url has been visited already, False otherwise
        '''
        pass

    @abc.abstractmethod
    def save_url(self, url, match_text=None):
        '''
        store the url (together with match_text) as having been visited.
        '''
        pass

    @abc.abstractmethod
    def connect(self, *condetails, **kwargs):
        '''
        connect with the given condetails (and/or kwargs) to the backend.
        '''
        pass

    @abc.abstractmethod
    def connected(self):
        '''
        @return True if a valid connection was established, False otherwise
        '''
        pass
