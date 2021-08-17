
from . import *
##########################################################################
##########################################################################
class RegisterForm(FlaskForm):
    first_name=StringField('First Name', validators=[DataRequired()])
    middle_name=StringField('Middle Name', validators=[DataRequired()])
    last_name=StringField('Last Name', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm= PasswordField('Confirm Password')
##########################################################################
##########################################################################
class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
##########################################################################
##########################################################################
class TasksForm(FlaskForm):
    # 'id','name','description','date','status'
    name=StringField('Name',validators=[DataRequired()])
    description=StringField('Description',validators=[DataRequired()])
    date=DateField('Due Date',validators=[DataRequired()])
    status= SelectField('status',choices = [('ongoing', 'ongoing'), ('closed', 'closed')],validators=[DataRequired()])
    
##########################################################################
##########################################################################
class TasksFormNot(FlaskForm):
    class Meta:
        csrf = False
    # 'id','name','description','date','status'
    id=HiddenField('id',validators=[DataRequired()])
    name=StringField('Name',validators=[DataRequired()])
    description=StringField('Description',validators=[DataRequired()])
    date=DateField('Due Date',validators=[DataRequired()])
    status= SelectField('status',choices = [('ongoing', 'ongoing'), ('closed', 'closed')],validators=[DataRequired()])
   
##########################################################################
##########################################################################
class AdminForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),])
##########################################################################
##########################################################################
