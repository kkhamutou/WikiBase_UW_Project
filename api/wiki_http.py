# wiki_http.py
import requests
import json
# import logging
#
# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
# logger.setLevel(logging.DEBUG)
#
#
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
#
# logger.addHandler(stream_handler)


class WikiHttp:

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
        params = WikiHttp._PARAMS
        params['titles'] = '|'.join(words) if type(words) == list else words
        # logger.info(params['titles'])
        response = requests.get(url=WikiHttp._URL, params=params, timeout=15)
        js = json.loads(response.text)
        return js


if __name__ == '__main__':
    x = WikiHttp()
    res = x.get('[][][]')
    print(json.dumps(res['query'], indent=4, sort_keys=True))