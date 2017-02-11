from app import db
import json
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#from enum import Enum

#class StatusEnum(Enum):
#    off = "off"
#    on = "on"

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

class Repository(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	key = db.Column(db.String(90))
	watcher_id = db.Column(db.Integer, db.ForeignKey('watcher.id'))
	watcher = db.relationship("Watcher", back_populates="repositories")
	create = db.Column(db.DateTime)
	add = db.Column(db.DateTime)
	push = db.Column(db.DateTime)
	text_raw = db.Column(db.Text(convert_unicode = True))
	text = db.Column(db.Text(convert_unicode = True))
			
	def __repr__(self):
		return self.text

class Watcher(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))	
	repository = db.Column(db.Boolean, default=False)
	push = db.Column(db.Boolean, default=False)
	params = db.Column(db.JSON)
	service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
	service = db.relationship("Service", back_populates="watchers")
	application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
	application = db.relationship("Application", back_populates="watchers")
	repositories = db.relationship("Repository", order_by=Repository.id, back_populates="watcher")

	def __repr__(self):
		return self.name

class Service(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	api = db.Column(db.String(100), nullable=False)
	status = db.Column(db.DateTime)
	params = db.Column(db.JSON)
	watchers = db.relationship("Watcher", order_by=Watcher.id, back_populates="service", cascade="all, delete, delete-orphan")

	def __repr__(self):
		return self.api

class Application(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	status = db.Column(db.DateTime)
	params = db.Column(db.JSON)
	watchers = db.relationship("Watcher", order_by=Watcher.id, back_populates="application")
	
	def __repr__(self):
		return self.name

