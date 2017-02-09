#!/usr/bin/python

import sys, time
from sqlalchemy.orm import joinedload, subqueryload, contains_eager, undefer
from app import app, db
from app.service import factory as serviceFactory
from app.models import Service, Watcher, Repository
from config import DEAMON_SLEEP_TIME

def run():
	while True:
		api = serviceFactory('watcher')
		for watcher in Watcher.query.all():
			if watcher.service is not None and watcher.service.repository == True:				
				try:
					f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
					if f is not None:
						f = f.key
				except NoResultFound as e:
					f = None

			pulled = api.pull(f, watcher, watcher.service)
			print pulled
			if pulled > 0:
				db.session.commit()
			
		time.sleep(DEAMON_SLEEP_TIME)

if __name__ == "__main__":
	run();
