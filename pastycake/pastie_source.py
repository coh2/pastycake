import httplib2

from lxml.html import parse

from .pastesource import PasteSource


class PastieSource(PasteSource):
    baseurl = 'http://pastie.org'

    def new_urls(self, backend):
        doc = parse('http://pastie.org/pastes').getroot()

        for link in doc.cssselect('div.pastePreview a'):
            app = link.get('href')

            if not backend.already_visited_url(app):
                yield self, app

    def get_paste(self, path):
        http = httplib2.Http()
        return http.request(path + '/text')

    def full_url(self, path):
        return path
