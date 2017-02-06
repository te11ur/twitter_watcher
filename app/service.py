from app import app, db
from models import User, Application, Service, Watcher, Repository
from app.api import factory as apiFactory
from datetime import datetime
import json

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
				keys = [r.key for r in Repository.query.all()]
				pulled = self.pull(keys, watcher, service)
				
				if pulled > 0:
					db.session.commit()
			#if service.push == True:
				#pushed = self.push(watcher)
			
		return { 'pulled': str(pulled), 'pushed': str(pushed)}
		
	def pull(self, keys, watcher, service):
		api = apiFactory(service.api, service.params)
		if api is None:
			return 0;
		
		
		count = 0;
		for key, post in api.read(watcher.params):
			try:
				index = keys.index(key)
			except ValueError:
				db.session.add(Repository(key=key, watcher_id = watcher.id, create = post['create'], text_raw = post['text_raw'], text = post['text'], add = datetime.utcnow()))
				count += 1
			
		return count
		
