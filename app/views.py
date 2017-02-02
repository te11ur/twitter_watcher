from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, ApplicationForm
from models import User, Application
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
		if form.delete.data > 0:
			application = db.session.query(Application).get(form.delete.data)
			if application is None:
				flash('Cannot delete application: ' + form.delete.data)
			else:
				db.session.delete(application)
			return redirect(url_for('applications', page = page))

		if form.id.data	> 0:
			application = session.query(Application).get(form.id.data)
			if application is None:
				flash('Cannot edit application: ' + form.id.data)
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
