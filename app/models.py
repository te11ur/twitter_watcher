from app import db
import json
#from enum import Enum

#class StatusEnum(Enum):
#    off = "off"
#    on = "on"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(64))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return self.email

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
	repository = db.Column(db.Boolean, default=False)
	push = db.Column(db.Boolean, default=False)
	status = db.Column(db.DateTime)
	params = db.Column(db.JSON)
	enabled = db.Column(db.Boolean, default=False)
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

