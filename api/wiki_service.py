#!api/wiki_service.py python3
"""
In this module, I tried to implement Facade pattern.
A facade is an object (here 'WikiService') that servisse as a front-facing interface masking more complex
underlying or structural code.

In this case, WikiService masks as a composition WikiHttp, ParsingResponse and Repository objects.

"""

from api.response import *
from api.wiki_http import WikiHttp
from repository.db_setup import Repository
from constants import DB_PATH


class WikiService:
    """Represent Facade for WikiHttp and Repository.
    Args:
         wiki_http - WikiHttp object that requests words from WikiService
         repo - Repository object (database)
    """

    def __init__(self, wiki_http: WikiHttp, repo: Repository):
        self.wiki_http = wiki_http
        self.repo = repo

    @staticmethod
    def _normalized_words(words: list or str):
        """Normalized words according to MediaWiki proposal:
            1. First letter is capital (First letter of a sentence, phrase of word. All others are up to the input
                since MediaWiki is case sensitive)
            2. Replace _ with white space
            3. Trim both sides
        """
        normalized_words = []
        words = [words] if type(words) != list else words

        for word in words:
            normalized_word = word.replace('_', ' ').strip()
            normalized_word = normalized_word[0].capitalize() + normalized_word[1:]
            if normalized_word not in normalized_words:
                normalized_words.append(normalized_word)

        return normalized_words

    def get_meanings_from_wiki(self, words):
        """Get response from MediaWiki and parse it. The proper result is uploaded to database.
            Args:
                words: list of string to be search in MeadiWiki
            Returns:
                tuple of successful and failed responses: len(tuple) == 2
        """
        normalized_words = WikiService._normalized_words(words)

        meanings = ResponseParser(self.wiki_http.get(normalized_words))
        succeed = list(filter(lambda k: isinstance(k, SuccessfulResponse), meanings))
        failed = list(filter(lambda k: not isinstance(k, SuccessfulResponse), meanings))
        for meaning in succeed:
            self.repo.insert(title=meaning.title, meaning=meaning.meaning,
                             page_id=meaning.page_id, search_word=meaning.search_word)

        return succeed, failed

    def check_database(self, words) -> list:
        """Check the list of words by search_word  the database and return those that are not listed."""
        normalized_words = tuple(WikiService._normalized_words(words))
        search_words = self.repo.find_by_search_word(normalized_words)
        missing_words = list(set(normalized_words) - set(getattr(attr, 'search_word') for attr in search_words))
        return missing_words


if __name__ == '__main__':

    service = WikiService(wiki_http=WikiHttp(),
                          repo=Repository(DB_PATH))
    res = service.get_meanings_from_wiki('Facade pattern')
    print(res)

