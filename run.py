#!/usr/bin/python
from app import app

if __name__ == '__main__':
	from config import SERVER_HOST, SERVER_PORT, DEBUG
	app.run(host=SERVER_HOST, port=SERVER_PORT, debug = DEBUG)
