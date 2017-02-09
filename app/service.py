from app import app, db
from sqlalchemy.orm.exc import NoResultFound
from models import User, Application, Service, Watcher, Repository
from app.api import factory as apiFactory
from datetime import datetime
from config import TIMEOUT_API
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
				try:
					f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
					if f is not None:
						f = f.key
				except NoResultFound as e:
					f = None
				pulled = self.pull(f, watcher, service)
				
				if pulled > 0:
					db.session.commit()
			#if service.push == True:
				#pushed = self.push(watcher)
			
		return { 'pulled': str(pulled), 'pushed': str(pushed)}
		
	def pull(self, key, watcher, service):
		api = apiFactory(service.api, service.params, TIMEOUT_API)
		if api is None:
			return 0;
			
		count = 0;
		for k, post in api.read(key, watcher.params):
			db.session.add(Repository(key=k, watcher_id = watcher.id, create = post['create'], text_raw = post['text_raw'], text = post['text'], add = datetime.utcnow()))
			count += 1
			
		return count
		
