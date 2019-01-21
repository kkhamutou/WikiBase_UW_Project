import pathlib

_MY_WINDOWS_PATH = 'C:/Users/KKhamutou/IdeaProjects/WikiBase_UW_Project/repository/test_db.db'
_MY_MAC_PATH = '/Users/kirylkhamutou/IdeaProjects/WikiBase_UW_Project/repository/test_db.db'


def _set_db_path():
    return str(pathlib.Path(__file__).parent / 'repository/test_db.db')


DB_PATH = _set_db_path()

if __name__ == '__main__':
    print(pathlib.Path(__file__).parent / 'repository/test_db.db')
