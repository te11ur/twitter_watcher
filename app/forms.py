from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, HiddenField, BooleanField, SelectField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	openid = TextField('Openid', validators = [Required()])
	remember_me = BooleanField('Remember_me', default = False)

class ApplicationForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	name = TextField('Name', validators = [Required()])

class ServiceForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	command = TextField('Command', validators = [Required()])
	repository = BooleanField('Repository', default = True)
	push = BooleanField('Push', default = False)
	enabled = BooleanField('Enabled', default = True)

class WatcherForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	name = TextField('Name', validators = [Required()])
	application = SelectField('Application', validators = [Required()], coerce = int)
	service = SelectField('Service', validators = [Required()], coerce = int)
