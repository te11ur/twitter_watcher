import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
#app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models, service
