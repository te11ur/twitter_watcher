#!/usr/bin/python
from app import app
from werkzeug.contrib.fixers import ProxyFix
from config import SERVER_HOST, SERVER_PORT, DEBUG

if __name__ == '__main__':
	app.run(host=SERVER_HOST, port=SERVER_PORT, debug = DEBUG)
