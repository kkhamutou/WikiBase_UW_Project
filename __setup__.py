from api.wiki_service import WikiService
from api.wiki_http import WikiHttp
from repository.db_setup import Repository
from constants import DB_PATH
import pathlib


def demo_setup():

    service = WikiService(wiki_http=WikiHttp(), repo=Repository(DB_PATH))

    with open(pathlib.Path(__file__).parent / 'test_cases/words', 'r') as file:
        words = file.read().split('\n')
    print(words[15:])

    demo = service.check_database(words)
    if len(demo) > 15:
        service.get_meanings_from_wiki(demo[0:15])
        service.get_meanings_from_wiki(demo[15:])
    else:
        service.get_meanings_from_wiki(demo)


if __name__ == '__main__':
    demo_setup()