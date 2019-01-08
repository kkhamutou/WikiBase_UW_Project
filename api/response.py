#!api/response.py python3
"""
In this module, I would like to show the  open/closed principle (LSP).
The principle state tat "software entities should be open for extension, but closed for modification".

Based on this principle, I tried to delegate the logic for each particular type of response to its corresponding class.
Then, I added a new polymorphic method to each type of response with the single responsibility of determining if
it corresponds to the data being passed or not, and I also have to change the logic to go through all responds,
finding the right one.

The important to notice that the interaction is now oriented toward an abstraction (base class Response).

Example of JSON produced by WikiMedia:
    The following wordes were searched:
        1. Python Programming
        2. This is missing
        3. []This[]is[]invalid[]
        4. Python
    The following output was given:
{
    "batchcomplete": "",
    "query": {
        "pageids": [
            "-2",
            "-1",
            "46332325",
            "23862"
        ],
        "pages": {
            "-1": {
                "invalid": "",
                "invalidreason": "The requested page title contains invalid characters: \"[\".",
                "title": "[]This[]is[]invalid[]"
            },
            "-2": {
                "missing": "",
                "ns": 0,
                "title": "This is missing"
            },
            "23862": {
                "extract": "Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, notably using significant whitespace. It provides constructs that enable clear programming on both small and large scales.",
                "ns": 0,
                "pageid": 23862,
                "title": "Python (programming language)"
            },
            "46332325": {
                "extract": "Python may refer to:",
                "ns": 0,
                "pageid": 46332325,
                "pageprops": {
                    "disambiguation": ""
                },
                "title": "Python"
            }
        },
        "redirects": [
            {
                "from": "Python Programming",
                "to": "Python (programming language)"
            }
        ]
    }
}

The class ResponseParser will store
['MissingResponse', 'InvalidResponse', 'DisambiguationResponse', 'SuccessfulResponse']
for every page received from WikiMedia.

In case if any particular response is out of the option, 'UnknownResponse' will be returned.

"""


class Response:
    """Base class for WikiMedia responses."""

    def __init__(self, page_id,  **kwargs):
        self.page_id = int(page_id)
        self.title = kwargs.get('title')

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.__dict__)

    @staticmethod
    def meets_condition(page_id, page) -> bool:
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
    def _identify_response(page_id, page: dict) -> Response:
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
    data = x.get(['Python Programming', 'This is missing', '[]This[]is[]invalid[]', 'Python'])
    y = ResponseParser(data)
    print(y[0].title)
    print(y)
