import sqlite3
import logging
from collections import namedtuple

logger = logging.getLogger('repository.db_setup')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
logger.setLevel(logging.DEBUG)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)


class Repository:

    _FILTER_CRITERIA = {'Is equal to': "='{}'",
                        'Is not equal to': "!='{}'",
                        'Starts with': "LIKE '{}%'",
                        'Does not contain': "NOT LIKE '%{}%'",
                        'Contains': "LIKE '%{}%'",
                        'Ends with': "LIKE '%{}'",
                        'Greater': ">'{}'",
                        'Greater or equal to': ">='{}'",
                        'Less': "<'{}'",
                        'Less or equal to': "<='{}'"}

    def __init__(self, db_path=':memory:'):
        try:
            self.connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            logger.exception(e)
            raise

        self.connection.row_factory = Repository._namedtuple_factory
        self.cursor = self.connection.cursor()

        self.cursor.executescript("""
                                PRAGMA foreign_keys = ON;
                                
                                CREATE TABLE IF NOT EXISTS tbl_wiki (
                                tbl_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                page_id INTEGER UNIQUE CHECK(TYPEOF(page_id) = 'integer' AND page_id >= 0), 
                                title TEXT NOT NULL CHECK(TYPEOF(title) = 'text' AND title != ''), 
                                search_word TEXT, 
                                meaning TEXT,
                                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                                
                                CREATE TABLE IF NOT EXISTS tbl_wiki_meaning (
                                tbl_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                wiki_id INTEGER, 
                                meaning TEXT NOT NULL CHECK(TYPEOF(meaning) = 'text' AND meaning != ''), 
                                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                                FOREIGN KEY(wiki_id) REFERENCES tbl_wiki(tbl_id) ON DELETE CASCADE);
                                """)

    @staticmethod
    def _namedtuple_factory(cursor, row) -> namedtuple:
        fields = [col[0] for col in cursor.description]
        Row = namedtuple("Row", fields)
        return Row(*row)

    def _find_by(self, field: str, values: tuple) -> list:
        r = self.cursor.execute(f"SELECT * FROM tbl_wiki WHERE {field} IN ({','.join(['?']*len(values))})", values)
        res = r.fetchall()
        return res

    def insert(self, title: str, meaning: str, search_word=None, page_id=None) -> None:

        if search_word is None:
            search_word = title

        try:
            self.cursor.execute('BEGIN')
            self.cursor.execute('INSERT INTO tbl_wiki(page_id, title, meaning, search_word) '
                                'VALUES(?, ?, ?, ?)', (page_id, title, meaning, search_word))
            self.cursor.execute('COMMIT')

        except self.connection.Error:
            self.cursor.execute('ROLLBACK')
            logger.exception("Exception occurred")

    def delete(self, _id: tuple) -> None:
        self.cursor.execute(f"DELETE FROM tbl_wiki WHERE tbl_id IN ({','.join(['?']*len(_id))})", _id)
        self.connection.commit()

    def find_by_id(self, _id: tuple) -> list:
        return self._find_by('tbl_id', _id)

    def find_by_page_id(self, page_id: tuple) -> list:
        return self._find_by('page_id', page_id)

    def find_by_title(self, title: tuple) -> list:
        return self._find_by('title', title)

    def find_by_search_word(self, search_word: tuple) -> list:
        return self._find_by('search_word', search_word)

    def find_all(self) -> list:
        return self.cursor.execute('SELECT * FROM tbl_wiki').fetchall()

    def filter_by(self, field: tuple, criteria: tuple, value: tuple) -> list:

        if all(len(lst) != len(field) for lst in [field, criteria, value]):
            raise IndexError('Length of args must be equal.')

        if not all(c in Repository._FILTER_CRITERIA for c in criteria):
            raise ValueError('Incorrect criteria: {}'.format(criteria))

        sql = "SELECT * FROM tbl_wiki WHERE "

        for f, c, v in zip(field, criteria, value):

            sql += '{} {} AND '.format('date({})'.format(f) if 'date' in f else f,
                                       Repository._FILTER_CRITERIA[c].format(v))
        sql = sql[0:len(sql) - len(' AND ')]

        res = self.cursor.execute(sql)
        return res.fetchall()


if __name__ == '__main__':

    x = Repository('/Users/kirylkhamutou/IdeaProjects/WikiBase_UW_Project/repository/test_db.db')
    r = x.filter_by(('created_date', 'title'), ('Is not equal to', 'Is not equal to'), ('2018-15-55', 'Berlin'))

    print(r)
