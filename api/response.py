"""
Algebraic data types
Search word field
"""
import requests
import json


class Response:

    def __init__(self, page_id, title):
        self.page_id = page_id
        self.title = title

    def __repr__(self):
            return '{}: {}\n'.format(self.__class__.__name__ ,self.__dict__.values())

    @staticmethod
    def parse_json(json):
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
                    res.append(SuccessfulResponse(pid, title, page['extract']))
            else:
                if 'missing' in page:
                    res.append(MissingResponse(pid, title))
                else:
                    res.append(InvalidResponse(pid, title, page['invalidreason']))

        return res


class MissingResponse(Response):

    def __init__(self, page_id, title):
        Response.__init__(self, page_id, title)
        self.is_missing = True


class DisambiguationResponse(Response):
    def __init__(self, page_id, title):
        Response.__init__(self, page_id, title)
        self.is_disambiguation = True


class InvalidResponse(Response):
    def __init__(self, page_id, title, reason):
        Response.__init__(self, page_id, title)
        self.reason = reason
        self.is_invalid = True



class SuccessfulResponse(Response):
    def __init__(self, page_id, title, meaning):
        Response.__init__(self, page_id, title)
        self.meaning = meaning

