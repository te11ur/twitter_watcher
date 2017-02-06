#!/usr/bin/python
 
import sys, time
from sqlalchemy.orm import joinedload, subqueryload, contains_eager, undefer
from app import app, db
from app.daemon import Daemon
from app.service import factory as serviceFactory
from app.models import Service, Watcher, Repository
from config import DEAMON_SLEEP_TIME
 
class WatcherDaemon(Daemon):
	def run(self):
		while True:
			api = serviceFactory('watcher')
			keys = [r.key for r in Repository.query.all()]
			for service in Service.query.options(subqueryload('watchers')).all():
				if service.repository == True:
					for watcher in service.watchers:
						pulled = self.pull(keys, watcher, service)
						if pulled > 0:
							db.session.commit()
						print str(pulled)
					
			time.sleep(DEAMON_SLEEP_TIME)
 
if __name__ == "__main__":
	daemon = WatcherDaemon('/tmp/daemon-watcher.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)