from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, HiddenField, BooleanField, SelectField, DateTimeField, TextAreaField, PasswordField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	email = TextField('email', description="Email", validators = [Required()])
	password = PasswordField('password', description="Password", validators = [Required()])

class RegisterForm(FlaskForm):
	email = TextField('email', description="Email", validators = [Required()])
	password = PasswordField('password', description="Password", validators = [Required()])
	password_repeat = PasswordField('repeat_password', description="Repeat password", validators = [Required()])

class ApplicationForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	name = TextField('name', validators = [Required()])
	params = TextAreaField('params')

class ServiceForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	api = TextField('API', validators = [Required()])
	repository = BooleanField('Repository', default = True)
	push = BooleanField('Push', default = False)
	params = TextAreaField('Params')
	enabled = BooleanField('Enabled', default = True)

class WatcherForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	name = TextField('Name', validators = [Required()])
	params = TextAreaField('Params', validators = [Required()])
	application = SelectField('Application', validators = [Required()], coerce = int)
	service = SelectField('Service', validators = [Required()], coerce = int)

class RepositoryForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	add = DateTimeField('Add', validators = [Required()])
	push = DateTimeField('Push', validators = [Required()])
	text_raw = TextAreaField('Text Raw')
	text = TextAreaField('Text')
	watcher = SelectField('Watcher', validators = [Required()], coerce = int)
