import json,time, os, random
from app import app, db
from sqlalchemy.orm.exc import NoResultFound
from models import User, Application, Service, Watcher, Repository
from app.api import factory as apiFactory
from datetime import datetime
from apns import APNs, Frame, Payload
from config import TIMEOUT_API, DEBUG

def factory(name):
	if name == 'watcher':
		return WatcherService()
	return None;
		
def response_listener(error_response):
    print "client get error-response: " + str(error_response)
	
class WatcherService():
	def run(self, id):
		watcher = db.session.query(Watcher).get(id)
		if watcher is None:
			return {'error': 'watcher with id: ' + id + ' not found'}
		
		

		pulled = 0;
		pushed = True;
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
				if self.push(f, watcher, application) == True:
					if DEBUG == True:
						print "Application {0} has new push notification\r\n".format(application.name)
					
					pushed = True
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
		
		apns = APNs(use_sandbox=True, enhanced=True, cert_file=os.path.join(basedir, 'apns/cert.pem'), key_file=os.path.join(basedir, 'apns/key.pem'))
		apns.gateway_server.register_response_listener(response_listener)
		#token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
		payload = Payload(alert=repository.text, sound="default", badge=1)
		identifier = random.getrandbits(32)
		for (token_hex, fail_time) in apns.feedback_server.items():
			print str(token_hex)
			apns.gateway_server.send_notification(token_hex, payload, identifier=identifier)
		return True
		
