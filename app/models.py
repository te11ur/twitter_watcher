from app import db
#from enum import Enum

#class StatusEnum(Enum):
#    off = "off"
#    on = "on"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
   #role = db.Column(db.SmallInteger, default = ROLE_USER)
   # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    watcher_id = db.Column(db.Integer, db.ForeignKey('watcher.id'))
    watcher = db.relationship("Watcher", back_populates="repositories")
    create = db.Column(db.Time)
    add = db.Column(db.Time)
    push = db.Column(db.Time)

    def __repr__(self):
        return "<Repository(create='%s')>" % self.create

class Watcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship("Service", back_populates="watchers")
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    application = db.relationship("Application", back_populates="watchers")
    repositories = db.relationship("Repository", order_by=Repository.id, back_populates="watcher")
   
    def __repr__(self):
        return "<Watcher(name='%s')>" % self.name

class Service(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    command = db.Column(db.String(100), nullable=False)
    repository = db.Column(db.Boolean, default=False)
    push = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('off', 'on', name='status_types'))
    enabled = db.Column(db.Boolean, default=False)
    watchers = db.relationship("Watcher", order_by=Watcher.id, back_populates="service", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Service(command='%s')>" % self.command

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    watchers = db.relationship("Watcher", order_by=Watcher.id, back_populates="application")

    def __repr__(self):
        return "<Application(name='%s')>" % self.name

