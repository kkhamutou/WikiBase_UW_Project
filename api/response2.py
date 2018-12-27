# response2.py
# open/close principle


class Response:
    """Base class for WikiMedia responses."""

    def __init__(self, page_id,  **kwargs):
        self.page_id = int(page_id)
        self.title = kwargs.get('title')

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.__dict__)

    @staticmethod
    def meets_condition(page_id, page):
        return False


class MissingResponse(Response):
    """Missing response from WikiMedia. The requested page is not found."""

    @staticmethod
    def meets_condition(page_id, page):
        return (
            int(page_id) <= 0
            and 'missing' in page
        )


class InvalidResponse(Response):
    """Invalid response from WikiMedia. The requested page title contains invalid characters: \"[\" or is empty."""

    @staticmethod
    def meets_condition(page_id, page):
        return (
                int(page_id) <= 0
                and 'invalidreason' in page
        )


class DisambiguationResponse(Response):
    """Disambiguation response from WikiMedia. More than one page exist in WikiMedia for a word searched."""

    @staticmethod
    def meets_condition(page_id, page):
        return (
            int(page_id) > 0
            and 'pageprops' in page
        )


class SuccessfulResponse(Response):
    """Successful response from WikiMedia. Meaning of a searched word has been found."""

    def __init__(self, page_id, **kwargs):
        """Named arguments from kwargs:
            extract: meaning of a word from JSON WikiMedia
            searchword: added key to the JSON.
                If redirects is NULL, searchword=title, otherwise searchword=redirects['from']"""

        super().__init__(page_id, **kwargs)
        self.meaning = kwargs.get('extract')
        self.search_word = kwargs.get('searchword')

    @staticmethod
    def meets_condition(page_id, page):
        return (
            int(page_id) > 0
            and 'pageprops' not in page
        )


class UnknownResponse(Response):
    """A type of response that cannot be identified from its data."""


class ResponseParser:
    """Parse JSON from WikiMedia and identify responses that occurred in the JSON."""

    def __init__(self, json: dict):

        self.page_ids = json['query']['pageids']
        self.pages = json['query']['pages']
        self.redirects = json['query']['redirects'] if 'redirects' in json['query'] else dict()
        self.data = list()

        # For every page in pages, key searchword is created to check if a word searched is redirected.
        # If a word search is  redirected, than searchword=redirects['from'], otherwise searchword=title.
        for page_id in self.page_ids:
            self.pages[page_id]['searchword'] = self._find_redirect_word(self.redirects, self.pages[page_id]['title'])
            self.data.append(self._identify_response(page_id, self.pages[page_id]))

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return str([cls.__class__.__name__ for cls in self.data])

    @staticmethod
    def _find_redirect_word(redirects: dict, word: str) -> str:
        for r in redirects:
            if r['to'] == word:
                return r['from']

        return word

    @staticmethod
    def _identify_response(page_id, page) -> object:
        for response_cls in Response.__subclasses__():
            try:
                if response_cls.meets_condition(page_id, page):
                    return response_cls(page_id, **page)
            except KeyError:
                continue

        return UnknownResponse(page_id)


if __name__ == '__main__':
    from api.wiki_http import WikiHttp

    x = WikiHttp()
    data = x.get(['[][][]', 'Python', 'Natzi', 'Kiryl', 'aSDASDA', '', 'My first word', 'Jack London'])

    y = ResponseParser(data)
    print(getattr(y[0], 'page_id'))

