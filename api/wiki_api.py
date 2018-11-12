"""
wiki_api.py is a module that contains classes & functions designed for the use of MediaWiki API.
Language of instruction: English
URL: http://en.wikipedia.org/w/api.php
password: NWMRaO

"""
import requests
import json
import time
from functools import wraps
import logging
from api import response as rs


log = logging.getLogger(__name__)


def retry(exceptions, tries=3, delay=3, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(func):

        @wraps(func)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    msg = '{}, Retrying in {} seconds...'.format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class MediaWiki:
    """
    The class is designed to call predefine API from MediaWiki (see http_get parameters).
    """

    _MEDIAWIKI_API_URL = 'http://en.wikipedia.org/w/api.php'

    def __init__(self, titles, retries=5):
        self.titles = '|'.join(titles) if type(titles) == list else titles
        self.retries = retries

    @retry(requests.exceptions.ConnectionError)
    def http_get(self):
        """
        Call HTTP Get method to request JSON from http://en.wikipedia.org/w/api.php.
        http_get returns dict() if data is fetched from MediaWiki, otherwise None.
        """

        params_wiki = {
            'action': 'query',              # Fetch data from and about MediaWiki.
            'prop': 'extracts|pageprops',   # Return plain-text or limited HTML extracts of the given pages|Page props.
            'ppprop': 'disambiguation',     # List page properties (return pageprops if page=disambiguation).
            'exintro': True,                # Return only content before the first section (type=boolean)
            'explaintext': True,            # Return extracts as plain text instead of limited HTML (type=boolean)
            'exsentences': 1,               # How many sentences to return (max=10, type=integer).
            'redirects': True,              # Automatically resolve redirects in query+titles (type=boolean).
            'titles': self.titles,          # A list of titles to work on (max=50).
            'indexpageids': True,           # Include pageids section listing all returned page IDs (type=boolean)
            'format': 'json'}               # The format of the output (JSON).

        response = requests.get(url=MediaWiki._MEDIAWIKI_API_URL, params=params_wiki, timeout=15)

        js = json.loads(response.text)
        return js


if __name__ == '__main__':
    word = ['Python Programming Language',
            'Jean Paul Sartre', 'Dance', 'Mercury', 'CEO', 'Montgomery']

    word = ['aksldjalksjdkl', '[][][]', 'Python', 'Python Programming', '']

    x = MediaWiki(word)
    r = x.http_get()

    print(json.dumps(r, indent=4))

    print(rs.Response.parse_json(r))
