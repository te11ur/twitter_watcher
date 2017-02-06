import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://twitter_watch:zsexdr@localhost/twitter_watcher'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SERVER_HOST = 'localhost'
SERVER_PORT = 80
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
POSTS_PER_PAGE = 10
DEAMON_SLEEP_TIME = 5

CONSUMER_KEY = 'Iq66eQcFgqFj0u4iuUiw7RI7I'
CONSUMER_SECRET = 'HGIIyeAzZxahrmCYn05JquAP5StIIGaBsK8DrtzUs4JBYsoET8'
ACCESS_TOKEN = '826439552034279424-4GUxKg83KlUgbggI4kaKlU9KwRavENY'
ACCESS_TOKEN_SECRET = 'YEzQ0PKQ3C92UMwVoFU3L0811e2cEQITeUAQA4HqMVzH5'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
