DEBUG = True

USERNAME = 'root'
PASSWORD = 'root'
SERVER = 'mysql'
DB = 'db_anunbis'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{SERVER}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = True
