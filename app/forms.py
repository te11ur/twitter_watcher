from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, HiddenField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	openid = TextField('Openid', validators = [Required()])
	remember_me = BooleanField('Remember_me', default = False)

class ApplicationForm(FlaskForm):
	id = HiddenField('Id')
	delete = HiddenField('delete')
	name = TextField('Name', validators = [Required()])
