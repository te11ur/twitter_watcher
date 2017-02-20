from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from app import app, db, lm
from app.service import factory as serviceFactory
from forms import LoginForm, RegisterForm, ApplicationForm, ServiceForm, WatcherForm, RepositoryForm, TokenForm
from models import User, Application, Service, Watcher, Repository, Token
from datetime import datetime
from config import POSTS_PER_PAGE
import json

pages = [
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
	},
	{ 
	    'url': 'tokens', 
	    'title': 'Tokens' 
	}
]

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/<string:watch>')
@app.route('/<string:watch>/<int:page>')
@app.route('/<string:watch>/<int:page>/<int:count>')
def index(watch = None, page=1, count = POSTS_PER_PAGE):
	pages = Repository.query.filter(Repository.watcher.has(name = watch)).\
		order_by(Repository.create.desc()).\
		paginate(page, count)
		
	def decript_entity(entity):
		try: 
			return json.loads(entity)
		except ValueError as e:
			return {}
		except TypeError as e:
			return {}
			
	return jsonify({
			'page': str(pages.page or 1),
			'prev': str(pages.prev_num),
			'next': str(pages.next_num),
			'total_pages': str(pages.pages),
			'per_page': str(pages.per_page),
			'result': [{ 
			'id': r.id,
			'key': r.key,
			'create': '' if r.create == None else r.create.strftime("%Y-%m-%d %H:%M:%S"),
			'add': '' if r.add == None else r.add.strftime("%Y-%m-%d %H:%M:%S"),
			'push': '' if r.push == None else r.push.strftime("%Y-%m-%d %H:%M:%S"),
			'text': r.text,
			'entities': decript_entity(r.text_raw)
		} for r in pages.items]});

@app.route('/admin')
@app.route('/admin/index')
@login_required
def admin():
	return render_template('index.html', title = 'Home', pages = pages)

@app.route('/tokens/<string:token>')
def tokens_add(token):

	if token is None or len(token) != 64:
		return jsonify(error = 'token invalid');
	try:	
		f = Token.query.filter(Token.token == token).first()
	except NoResultFound as e:
		f = None
	
	if f is not None:
		return jsonify(error = 'token exists');
		
	token = Token(token = token, enabled = True)
	db.session.add(token)
	db.session.commit()	
	return jsonify(ok='ok');
	

@app.route('/admin/tokens', methods = ['GET', 'POST'])
@app.route('/admin/tokens/<int:page>', methods = ['GET', 'POST'])
@login_required
def tokens(page=1):
	form = TokenForm()
	if request.method == 'POST':
		if form.delete.validate(form):
			try:
				deleteId = int(form.delete.data);
			except ValueError as e:
				deleteId = 0
			if deleteId > 0:
				token = db.session.query(Token).get(deleteId)
				if token is None:
					flash('Cannot delete token: ' + str(deleteId))
				else:
					db.session.delete(token)
					db.session.commit()
				return redirect(url_for('token', page = page))

		if form.validate():
			try:
				editId = int(form.id.data);
			except ValueError as e:
				editId = 0

			if editId > 0:
				token = db.session.query(Token).get(editId)
				if token is None:
					flash('Cannot edit token: ' + str(editId))
				else:
					token.token = form.token.data
					token.enabled = form.enabled.data
					db.session.commit()
				return redirect(url_for('tokens', page = page))
			
			token = Token(token = form.token.data, enabled = form.enabled.data)
			db.session.add(token)
			db.session.commit()
			flash('Your token is now live!')
			return redirect(url_for('tokens', page = page))
		else:
			flash('No data')
			return redirect(url_for('tokens', page = page))
			
	
	tokens = Token.query.order_by('id').paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = tokens, fields = ['id', 'token', 'enabled'], title = 'Token', model = 'token', route = 'tokens')

@app.route('/admin/applications', methods = ['GET', 'POST'])
@app.route('/admin/applications/<int:page>', methods = ['GET', 'POST'])
@login_required
def applications(page=1):
	form = ApplicationForm()
	if request.method == 'POST':
		if form.delete.validate(form):
			try:
				deleteId = int(form.delete.data);
			except ValueError as e:
				deleteId = 0
			if deleteId > 0:
				application = db.session.query(Application).get(deleteId)
				if application is None:
					flash('Cannot delete application: ' + str(deleteId))
				else:
					db.session.delete(application)
					db.session.commit()
				return redirect(url_for('applications', page = page))

		if form.validate():
			try:
				editId = int(form.id.data);
			except ValueError as e:
				editId = 0

			if editId > 0:
				application = db.session.query(Application).get(editId)
				if application is None:
					flash('Cannot edit application: ' + str(editId))
				else:
					application.name = form.name.data
					application.params = form.params.data
					db.session.commit()
				return redirect(url_for('applications', page = page))
			
			application = Application(name = form.name.data, params = form.params.data)
			db.session.add(application)
			db.session.commit()
			flash('Your application is now live!')
			return redirect(url_for('applications', page = page))
		else:
			flash('No data')
			return redirect(url_for('applications', page = page))
			
	
	applications = Application.query.order_by('id').paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = applications, fields = ['id', 'name', 'params', 'status'], title = 'Application', model = 'application', route = 'applications')

@app.route('/admin/services', methods = ['GET', 'POST'])
@app.route('/admin/services/<int:page>', methods = ['GET', 'POST'])
@login_required
def services(page=1):
	form = ServiceForm()
	if request.method == 'POST':
		if form.delete.validate(form):
			try:
				deleteId = int(form.delete.data);
			except ValueError as e:
				deleteId = 0

			if deleteId > 0:
				service = db.session.query(Service).get(deleteId)
				if service is None:
					flash('Cannot delete service: ' + str(deleteId))
				else:
					db.session.delete(service)
					db.session.commit()
				return redirect(url_for('services', page = page))
		if form.validate():
			try:
				editId = int(form.id.data);
			except ValueError as e:
				editId = 0

			if editId > 0:
				service = db.session.query(Service).get(editId)
				if service is None:
					flash('Cannot edit service: ' + str(editId))
				else:
					service.api = form.api.data
					service.params = form.params.data
					db.session.commit()
				return redirect(url_for('services', page = page))
			
			service = Service(api = form.api.data, params = form.params.data)
			db.session.add(service)
			db.session.commit()
			flash('Your services is now live!')
			return redirect(url_for('services', page = page))
		
		else:
			flash('No data')
			return redirect(url_for('services', page = page))
	
	services = Service.query.order_by('id').paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = services, fields = ['id', 'api', 'params', 'status'], title = 'Service', model = 'service', route = 'services')

@app.route('/admin/watchers', methods = ['GET', 'POST'])
@app.route('/admin/watchers/<int:page>', methods = ['GET', 'POST'])
@login_required
def watchers(page=1):
	form = WatcherForm()
	form.application.choices = [(a.id, a.name) for a in Application.query.order_by('id')]
	form.service.choices = [(s.id, s.api) for s in Service.query.order_by('id')]

	if request.method == 'POST':
		if form.delete.validate(form):
			try:
				deleteId = int(form.delete.data);
			except ValueError as e:
				deleteId = 0
			if deleteId > 0:
				watcher = db.session.query(Watcher).get(deleteId)
				if watcher is None:
					flash('Cannot delete watcher: ' + str(deleteId))
				else:
					db.session.delete(watcher)
					db.session.commit()
				return redirect(url_for('watchers', page = page))
		if form.validate():
			try:
				editId = int(form.id.data);
			except ValueError as e:
				editId = 0

			if editId > 0:
				watcher = db.session.query(Watcher).get(editId)
				if watcher is None:
					flash('Cannot edit watcher: ' + str(editId))
				else:
					watcher.name = form.name.data
					watcher.repository = form.repository.data
					watcher.push = form.push.data
					watcher.application_id = form.application.data
					watcher.service_id = form.service.data
					watcher.params = form.params.data
					watcher.push_params = form.push_params.data
					db.session.commit()
				return redirect(url_for('watchers', page = page))
			
			watcher = Watcher(name = form.name.data, repository = form.repository.data, push = form.push.data, application_id = form.application.data, service_id = form.service.data, params = form.params.data, push_params = form.push_params.data)
			db.session.add(watcher)
			db.session.commit()
			flash('Your watcher is now live!')
			return redirect(url_for('watchers', page = page))
		else:
			flash('No data')
			return redirect(url_for('watchers', page = page))

	watchers = Watcher.query.order_by('id').paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = watchers, fields = ['id', 'name', 'repository', 'push', 'params', 'push_params', 'application', 'service'], title = 'Watcher', model = 'watcher', route = 'watchers')

@app.route('/admin/repositories', methods = ['GET', 'POST'])
@app.route('/admin/repositories/<int:page>', methods = ['GET', 'POST'])
@login_required
def repositories(page=1):
	form = RepositoryForm()
	form.watcher.choices = [(w.id, w.name) for w in Watcher.query.order_by('id')]
	if request.method == 'POST':
		if form.delete.validate(form):
			try:
				deleteId = int(form.delete.data);
			except ValueError as e:
				deleteId = 0

			if deleteId > 0:
				repository = db.session.query(Repository).get(deleteId)
				if repository is None:
					flash('Cannot delete repository: ' + str(deleteId))
				else:
					db.session.delete(repository)
					db.session.commit()
				return redirect(url_for('repositories', page = page))
		if form.validate():
			try:
				editId = int(form.id.data);
			except ValueError as e:
				editId = 0

			if editId > 0:
				repository = db.session.query(Repository).get(editId)
				if repository is None:
					flash('Cannot edit repository: ' + str(editId))
				else:
					repository.watcher_id = form.watcher.data
					repository.add = form.add.data
					repository.push = form.push.data
					repository.text_raw = form.text_raw.data
					repository.text = form.text.data
					db.session.commit()
				return redirect(url_for('repositories', page = page))
			
			repository = Repository(watcher_id = form.watcher.data, add = form.add.data, push = form.push.data, text_raw = form.text_raw.data, text = form.text.data)
			db.session.add(repository)
			db.session.commit()
			flash('Your repository is now live!')
			return redirect(url_for('repositories', page = page))
		
		else:
			flash('No data')
			return redirect(url_for('repositories', page = page))

	repositories = Repository.query.order_by('id').paginate(page, POSTS_PER_PAGE, False);

	return render_template('list.html', pages = pages, form = form, elements = repositories, fields = ['id', 'key', 'watcher','create','add', 'push', 'text', 'text_raw'], title = 'Repository', model = 'repository', route = 'repositories')

@app.route('/admin/run/<string:model>/<int:id>')
#@login_required
def run(model, id):
	service = serviceFactory(model);
	if service is not None:
		return jsonify(service.run(id))
	
	return jsonify(error = 'no run with type ' + model + ' found');
'''
@app.route('/admin/register', methods=['GET', 'POST'])
def register():
	"""User registration route."""
	if current_user.is_authenticated:
		return redirect(url_for('admin'))

	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			flash('Username already exists.')
			return redirect(url_for('register'))

		user = User(email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('admin'))
	return render_template('register.html', title = 'Please sign out', form=form)
'''
@app.route('/admin/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('admin'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash('Invalid username or password.')
			return redirect(url_for('login'))

		login_user(user)
		flash('You are now logged in!')
		return redirect(url_for('admin'))
	return render_template('login.html', title = 'Please sign in', form = form)

@app.route('/admin/logout')
def logout():
	logout_user()
	return redirect(url_for('admin'))
