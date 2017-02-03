from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, ApplicationForm, ServiceForm, WatcherForm
from models import User, Application, Service, Watcher
from datetime import datetime
from config import POSTS_PER_PAGE

pages = [
	{ 
	    'url': 'index', 
	    'title': 'Start' 
	},
	{ 
	    'url': 'applications', 
	    'title': 'Applications' 
	},
	{ 
	    'url': 'services', 
	    'title': 'Services' 
	},
	{ 
	    'url': 'watchers', 
	    'title': 'Watchers' 
	},
	{ 
	    'url': 'repositories', 
	    'title': 'Repositories' 
	}
]

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	return render_template('empty.html')

@app.route('/admin')
@app.route('/admin/index')
#@login_required
def admin():
	#user = g.user
	return render_template('index.html', title = 'Home', pages = pages)

@app.route('/admin/applications', methods = ['GET', 'POST'])
@app.route('/admin/applications/<int:page>', methods = ['GET', 'POST'])
#@login_required
def applications(page=1):
	#user = g.user
	form = ApplicationForm()
	if form.validate_on_submit():

		try:
			deleteId = int(form.delete.data);
		except ValueError as e:
			deleteId = 0

		try:
			editId = int(form.id.data);
		except ValueError as e:
			editId = 0

		if deleteId > 0:
			application = db.session.query(Application).get(deleteId)
			if application is None:
				flash('Cannot delete application: ' + str(deleteId))
			else:
				db.session.delete(application)
				db.session.commit()
			return redirect(url_for('applications', page = page))

		if editId > 0:
			application = db.session.query(Application).get(editId)
			if application is None:
				flash('Cannot edit application: ' + str(editId))
			else:
				application.name = form.name.data
				db.session.commit()
			return redirect(url_for('applications', page = page))
			
		application = Application(name = form.name.data)
		db.session.add(application)
		db.session.commit()
		flash('Your application is now live!')
		return redirect(url_for('applications', page = page))
	
	applications = Application.query.paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = applications, fields = ['id', 'name'], title = 'Application', model = 'application', route = 'applications')


@app.route('/admin/services', methods = ['GET', 'POST'])
@app.route('/admin/services/<int:page>', methods = ['GET', 'POST'])
#@login_required
def services(page=1):
	#user = g.user
	form = ServiceForm()
	if form.validate_on_submit():

		try:
			deleteId = int(form.delete.data);
		except ValueError as e:
			deleteId = 0

		try:
			editId = int(form.id.data);
		except ValueError as e:
			editId = 0

		if deleteId > 0:
			service = db.session.query(Service).get(deleteId)
			if service is None:
				flash('Cannot delete service: ' + str(deleteId))
			else:
				db.session.delete(service)
				db.session.commit()
			return redirect(url_for('services', page = page))

		if editId > 0:
			service = db.session.query(Service).get(editId)
			if service is None:
				flash('Cannot edit service: ' + str(editId))
			else:
				service.command = form.command.data
				service.repository = form.repository.data
				service.push = form.push.data
				service.enabled = form.enabled.data
				db.session.commit()
			return redirect(url_for('services', page = page))
			
		service = Service(command = form.command.data, repository = form.repository.data, push = form.push.data, enabled = form.enabled.data, status = 'off')
		db.session.add(service)
		db.session.commit()
		flash('Your services is now live!')
		return redirect(url_for('services', page = page))
	
	services = Service.query.paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = services, fields = ['id', 'command', 'repository', 'push', 'enabled', 'status'], title = 'Service', model = 'service', route = 'services')


@app.route('/admin/watchers', methods = ['GET', 'POST'])
@app.route('/admin/watchers/<int:page>', methods = ['GET', 'POST'])
#@login_required
def watchers(page=1):
	#user = g.user
	form = WatcherForm()
	form.application.choices = [(a.id, a.name) for a in Application.query.order_by('id')]
	form.service.choices = [(s.id, s.command) for s in Service.query.order_by('id')]

	if form.validate_on_submit():

		try:
			deleteId = int(form.delete.data);
		except ValueError as e:
			deleteId = 0

		try:
			editId = int(form.id.data);
		except ValueError as e:
			editId = 0

		if deleteId > 0:
			watcher = db.session.query(Watcher).get(deleteId)
			if watcher is None:
				flash('Cannot delete watcher: ' + str(deleteId))
			else:
				db.session.delete(watcher)
				db.session.commit()
			return redirect(url_for('watchers', page = page))

		if editId > 0:
			watcher = db.session.query(Watcher).get(editId)
			if watcher is None:
				flash('Cannot edit watcher: ' + str(editId))
			else:
				watcher.name = form.name.data
				watcher.application = form.application.data
				watcher.service = form.service.data
				db.session.commit()
			return redirect(url_for('watchers', page = page))
			
		watcher = Watcher(name = form.name.data, application = form.application.data, service = form.service.data)
		db.session.add(watcher)
		db.session.commit()
		flash('Your watcher is now live!')
		return redirect(url_for('watchers', page = page))
	
	watchers = Watcher.query.paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = watchers, fields = ['id', 'name', 'application', 'service'], title = 'Watcher', model = 'watcher', route = 'watchers')


@app.route('/admin/login', methods = ['GET', 'POST'])
#@oid.loginhandler
def login():
	#if g.user is not None and g.user.is_authenticated:
		#return redirect(url_for('admin/index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('admin/login'))

	user = User.query.filter_by(email = resp.email).first()

	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname = nickname, email = resp.email)
		db.session.add(user)
		db.session.commit()

	remember_me = False

	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)

	login_user(user, remember = remember_me)

	return redirect(request.args.get('next') or url_for('admin/index'))

@app.route('/admin/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
