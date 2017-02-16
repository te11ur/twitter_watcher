#!/usr/bin/python

import sys, time
from sqlalchemy.orm import joinedload, subqueryload, contains_eager, undefer
from app import app, db
from app.service import factory as serviceFactory
from app.models import Service, Watcher, Repository
from config import DEAMON_SLEEP_TIME, DEBUG
from datetime import datetime

def run():
	while True:
		api = serviceFactory('watcher')
		for watcher in Watcher.query.all():
			pulled = 0
			pushed = 0
			f = None
			if watcher.repository == True:
				service = watcher.service				
				if service is not None:				
					try:
						f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
						if f is not None:
							f = f.key
					except NoResultFound as e:
						f = None

					pulled = api.pull(f, watcher, service)
					if pulled > 0:
						if DEBUG == True:
							print "Watcher {0} has new {1} rows\r\n".format(watcher.name, str(pulled))
							
						service.status = datetime.utcnow()
						db.session.commit()
			
			if watcher.push == True:
				application = watcher.application
				if application is not None:
					try:
						f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
					except NoResultFound as e:
						f = None	
						
					if f is not None and f.push is None:
						pushed = api.push(f, watcher, application)
						if pushed > 0:
							if DEBUG == True:
								print "Application %s has new %s pushs notification\r\n" % (application.name, pushed)
							
							f.push = datetime.utcnow()
							application.status = datetime.utcnow()
							db.session.commit()
		
		time.sleep(DEAMON_SLEEP_TIME)

if __name__ == "__main__":
	run();
