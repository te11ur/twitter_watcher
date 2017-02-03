from app import app, db
from models import User, Application, Service, Watcher, Repository
from app.api import factory as apiFactory
from datetime import datetime

def factory(name):
	if name == 'watcher':
		return WatcherService()
	return None;

class WatcherService():
	def run(self, id):
		watcher = db.session.query(Watcher).get(id)
		if watcher is None:
			return {'error': 'watcher with id: ' + id + ' not found'}
		
		service = watcher.service;
		if service is None:
			return {'error': 'watcher has no service'}

		pulled = 0;
		pushed = 0;
		if service.enabled == True:
			if service.repository == True:
				pulled = self.pull(watcher.id, service.command, watcher.name)
			#if service.push == True:
				#pushed = self.push(watcher)
			
		return { 'pulled': str(pulled), 'pushed': str(pushed)}
		
	def pull(self, watcherId, command, name):
		api = apiFactory(command)
		if api is None:
			return 0;
		
		count = 0;
		for post in api.read(name):
			db.session.add(Repository(watcher_id = watcherId, create = post['create'], add = datetime.utcnow()))
			count += 1
		db.session.commit()
		return count
		
