from flask_wtf import FlaskForm,Form
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField,PasswordField,SelectField,HiddenField
from wtforms.validators import DataRequired,Email,AnyOf,EqualTo,ValidationError
from wtforms.fields.html5 import DateField,DateTimeField