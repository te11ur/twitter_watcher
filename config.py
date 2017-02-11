import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://twitter_watch:zsexdr@127.0.0.1/twitter_watcher'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
POSTS_PER_PAGE = 10
DEAMON_SLEEP_TIME = 5
TIMEOUT_API = 10