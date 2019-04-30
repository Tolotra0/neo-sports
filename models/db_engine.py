from sqlalchemy import create_engine


database_credentials = {
    'domain': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'nsdb'
}

engine = create_engine('mysql+pymysql://{}:{}@{}/{}' . format(
    database_credentials['user'],
    database_credentials['password'],
    database_credentials['domain'],
    database_credentials['database']
), echo=False)