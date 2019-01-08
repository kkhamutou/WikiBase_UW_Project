#!api/wiki_http.py Python3
"""
This module contains WikiHttp class that does a request from MediaWiki.
Language of instruction: English
URL: http://en.wikipedia.org/w/api.php

Example:
    input words = 'Python Programming', 'This is missing', '[]This[]is[]invalid[]', 'Python'

    output dict:
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
"""
import requests
import json


class WikiHttp:
    """WikiHttp requests a JSON from MediaWiki based on words provided."""

    _PARAMS = {
        'action': 'query',              # Fetch data from and about MediaWiki.
        'prop': 'extracts|pageprops',   # Return plain-text or limited HTML extracts of the given pages|Page props.
        'ppprop': 'disambiguation',     # List page properties (return pageprops if page=disambiguation).
        'exintro': True,                # Return only content before the first section (type=boolean)
        'explaintext': True,            # Return extracts as plain text instead of limited HTML (type=boolean)
        'exsentences': 3,               # How many sentences to return (max=10, type=integer).
        'redirects': True,              # Automatically resolve redirects in query+titles (type=boolean).
        'indexpageids': True,           # Include pageids section listing all returned page IDs (type=boolean)
        'format': 'json'}               # The format of the output (JSON).

    _URL = 'http://en.wikipedia.org/w/api.php'

    def get(self, words):
        """
        Do request get from MediaWiki.
        Args:
                words: list or str of words
        Returns:
            dict: JSON serialization
        """
        params = WikiHttp._PARAMS
        params['titles'] = '|'.join(words) if type(words) == list else words
        # logger.info(params['titles'])
        response = requests.get(url=WikiHttp._URL, params=params, timeout=15)
        js = json.loads(response.text)
        return js


if __name__ == '__main__':
    x = WikiHttp()
    res = x.get(['Python Programming', 'This is missing', '[]This[]is[]invalid[]', 'Python'])
    print(res['query']['pages']['-1'])
    print(json.dumps(res, indent=4, sort_keys=True))
