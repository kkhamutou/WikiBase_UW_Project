"""
Algebraic data types
Search word field
Fc69Yh
"""


class Response:

    def __init__(self, page_id, title):
        self.page_id = page_id
        self.title = title

    def __repr__(self):
            return '{}: {}'.format(self.__class__.__name__, self.__dict__.items())

    @staticmethod
    def _find_redirect_word(redirects: dict, word: str):
        # return r['from'] for r in redirects if r['to'] == word else word
        for r in redirects:
            if r['to'] == word:
                return r['from']

        return word

    @staticmethod
    def parse_json(json) -> list:

        redirects = json['query']['redirects'] if 'redirects' in json['query'] else dict()
        page_ids = json['query']['pageids']  # list of page ids
        res = []

        for page_id in page_ids:
            page = json['query']['pages'][page_id]
            title = page['title']
            pid = int(page_id)

            if pid > 0:
                if 'pageprops' in page:
                    res.append(DisambiguationResponse(pid, title))
                else:
                    res.append(SuccessfulResponse(pid, title, page['extract'],
                                                  Response._find_redirect_word(redirects, title)))
            else:
                if 'missing' in page:
                    res.append(MissingResponse(pid, title))
                else:
                    res.append(InvalidResponse(pid, title, page['invalidreason']))

        return res


class MissingResponse(Response):
    def __init__(self, page_id, title):
        Response.__init__(self, page_id, title)


class DisambiguationResponse(Response):
    def __init__(self, page_id, title):
        Response.__init__(self, page_id, title)


class InvalidResponse(Response):
    def __init__(self, page_id, title, reason):
        Response.__init__(self, page_id, title)
        self.reason = reason


class SuccessfulResponse(Response):
    def __init__(self, page_id, title, meaning, search_word):
        Response.__init__(self, page_id, title)
        self.meaning = meaning
        self.search_word = search_word

