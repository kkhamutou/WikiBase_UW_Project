import sqlite3
import datetime
from api.wiki_api import MediaWiki


def connect(func):
    def wrapper(conn, *args, **kwargs):
        try:
            conn.execute()

db = sqlite3.connect(':memory:')
cursor = db.cursor()


cursor.execute('CREATE TABLE wiki (id INTEGER PRIMARY KEY AUTOINCREMENT, pageid INTEGER UNIQUE, created_date DATETIME, '
               '                    title TEXT, extract TEXT, reference INTEGER)')

sql = 'INSERT INTO wiki(pageid, created_date, title, extract, reference) VALUES(?, ?, ?, ?, ?)'

wiki = MediaWiki(['Economics', 'Poland', 'Luxoft', 'Communism', 'France', 'L']).http_get()

for key in wiki:
    cursor.execute(sql, [wiki[key]['pageid'], datetime.datetime.utcnow(),
                         wiki[key]['title'], wiki[key]['extract'], 1]
                   )

res = cursor.execute('SELECT title, extract FROM wiki').fetchall()

for row in res:
    print(row)

