"""
Input operation
SQLite - (tables, queries, ...)

"""

from api.response import *
from api.wiki_http import WikiHttp
from repository.db_setup import Repository


class WikiService:

    def __init__(self, wiki_http: WikiHttp, repo: Repository):
        self.wiki_http = wiki_http
        self.repo = repo

    @staticmethod
    def _normalized_words(words):
        normalized_words = []
        words = [words] if type(words) != list else words

        for word in words:
            normalized_word = word.replace('_', ' ').strip()
            normalized_word = normalized_word[0].capitalize() + normalized_word[1:]
            if normalized_word not in normalized_words:
                normalized_words.append(normalized_word)

        return normalized_words

    def get_meanings_from_wiki(self, words):
        normalized_words = WikiService._normalized_words(words)

        meanings = Response.parse_json(self.wiki_http.get(normalized_words))
        succeed = list(filter(lambda k: isinstance(k, SuccessfulResponse), meanings))
        failed = list(filter(lambda k: not isinstance(k, SuccessfulResponse), meanings))
        for meaning in succeed:
            self.repo.insert(title=meaning.title, meaning=meaning.meaning,
                             page_id=meaning.page_id, search_word=meaning.search_word)

        return succeed, failed

    def check_database(self, words) -> list:
        """Check the list of words in the database and return those that are not listed."""
        normalized_words = tuple(WikiService._normalized_words(words))
        search_words = self.repo.find_by_search_word(normalized_words)
        missing_words = list(set(normalized_words) - set(getattr(attr, 'search_word') for attr in search_words))
        return missing_words

    def filter_by(self, field, values):
        pass


if __name__ == '__main__':

    service = WikiService(wiki_http=WikiHttp(), repo=Repository())
    # service.repo.insert(title='Python', meaning='Programming Language', page_id=12345678, search_word='Python')
    x = service.get_meanings_from_wiki(['Python Programming Language'])

