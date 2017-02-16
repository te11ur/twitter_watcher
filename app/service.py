import json,time, os, random
from app import app, db
from sqlalchemy.orm.exc import NoResultFound
from models import User, Application, Service, Watcher, Repository, Token
from app.api import factory as apiFactory
from datetime import datetime
from apns import APNs, Frame, Payload
from config import TIMEOUT_API, DEBUG

def factory(name):
	if name == 'watcher':
		return WatcherService()
	return None;
		
class WatcherService():
	def run(self, id):
		watcher = db.session.query(Watcher).get(id)
		if watcher is None:
			return {'error': 'watcher with id: ' + id + ' not found'}
		
		

		pulled = 0;
		pushed = 0;
		if watcher.repository == True:
			service = watcher.service;
			if service is None:
				return {'error': 'watcher has no service'}
				
			try:
				f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
				if f is not None:
					f = f.key
			except NoResultFound as e:
				f = None
			pulled = self.pull(f, watcher, service)
			
			if pulled > 0:
				if DEBUG == True:
					print "Watcher {0} has new {1} rows\r\n".format(watcher.name, str(pulled))
				service.status = datetime.utcnow()
				db.session.commit()
		if watcher.push == True:
			application = watcher.application;
			if application is None:
				return {'error': 'watcher has no application'}
			try:
				f = Repository.query.filter(Repository.watcher.has(name = watcher.name)).order_by(Repository.create.desc()).first()
			except NoResultFound as e:
				f = None	
				
			if f is not None: #and f.push is None:
				pushed = self.push(f, watcher, application)
				if pushed > 0:
					if DEBUG == True:
						print "Application %s has new %s pushs notification\r\n" % (application.name, pushed)
					
					f.push = datetime.utcnow()
					application.status = datetime.utcnow()
					db.session.commit()
			
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
		
	def push(self, repository, watcher, application):
		basedir = os.path.abspath(os.path.dirname(__file__))
		try:
			params = json.loads(application.params)
		except ValueError as e:
			params = {}

		cert_file = params.get('cert_file')
		if cert_file is None:
			print 'Need cert_file'
			return 0

		params['cert_file'] = os.path.join(basedir, 'apns/%s/%s' % (application.name, cert_file))

		key_file = params.get('key_file')
		if key_file is None:
			print 'Need key_file'
			return 0

		params['key_file'] = os.path.join(basedir, 'apns/%s/%s' % (application.name, key_file))

		try:
			push_params = json.loads(watcher.push_params)
		except ValueError as e:
			push_params = {}
		except TypeError as e:
			push_params = {}
		
		push_params['alert'] = repository.text

		apns = APNs(**params)
		payload = Payload(**push_params)
		count = 0

		for token in db.session.query(Token):
			apns.gateway_server.send_notification(token.token, payload)
			count += 1
		return count
		
