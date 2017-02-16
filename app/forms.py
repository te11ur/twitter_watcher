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
	id = HiddenField('id')
	delete = HiddenField('delete')
	name = TextField('name', description="Name", validators = [Required()])
	params = TextAreaField('params', description="Params")

class ServiceForm(FlaskForm):
	id = HiddenField('id')
	delete = HiddenField('delete')
	api = TextField('api', description="API", validators = [Required()])
	params = TextAreaField('params', description="Params")

class WatcherForm(FlaskForm):
	id = HiddenField('id')
	delete = HiddenField('delete')
	name = TextField('name', description="Name", validators = [Required()])
	repository = BooleanField('repository', description="Add repository", default = True)
	push = BooleanField('push', description="Send Push", default = False)
	params = TextAreaField('params', description="Params", validators = [Required()])
	push_params = TextAreaField('push_params', description="Push params", validators = [Required()])
	application = SelectField('application', description="Application", validators = [Required()], coerce = int)
	service = SelectField('service', description="Service", validators = [Required()], coerce = int)

class RepositoryForm(FlaskForm):
	id = HiddenField('id')
	delete = HiddenField('delete')
	add = DateTimeField('add', description="Add time", validators = [Required()])
	push = DateTimeField('push', description="Push time", validators = [Required()])
	text_raw = TextAreaField('entities', description="Entities")
	text = TextAreaField('text', description="Text")
	watcher = SelectField('watcher', description="Watcher", validators = [Required()], coerce = int)

class TokenForm(FlaskForm):
	id = HiddenField('id')
	delete = HiddenField('delete')
	token = TextField('token', description="token", validators = [Required()])
