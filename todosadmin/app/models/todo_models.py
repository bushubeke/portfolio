
from re import U
from . import *

###########################################################################
    #this is the user model along with the user model methods
##########################################################################
class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,autoincrement="auto")
    email=Column(String(255), unique=True,nullable=False)
    first_name =Column(String(100),nullable=False)
    middle_name = Column(String(100),nullable=False)
    last_name= Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    date_registerd= Column(DateTime(),default=datetime.datetime.utcnow())
    tasks =relationship('Tasks', passive_deletes = True )#backref='users', lazy=True
    #authenticated = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<User '{self.first_name}'>"
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    def is_active(self):
        return True
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_anonymous(self):
        return False
###########################################################################
    #this is the Admin along with the Admin model methods
##########################################################################
class Admin(db.Model):
    """ Admin Model for storing app admin  related details """
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True,autoincrement="auto")
    username=Column(String(255),nullable=False)
    first_name =Column(String(100),nullable=False)
    middle_name = Column(String(100),nullable=False)
    last_name= Column(String(100),nullable=False)
    password = Column(String(500),nullable=False)
    def __repr__(self):
        return f"<User '{self.first_name}'>"

#############################################################################
    #this is tasks table with one to many relationship with along with its methods
############################################################################
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer(), primary_key=True,autoincrement="auto")
    name = Column(String(80))
    description = Column(String(255))
    date=Column(DateTime(),default=datetime.datetime.utcnow())
    status=Column(String(10),default="ongoing")
    user= Column('user_id', Integer(), ForeignKey('user.id',ondelete='cascade'))
    def __repr__(self):
        return f"{self.name}"
#############################################################################

##############################################################################################################
    #after this section marshmallow modle schemas can be definded
##############################################################################################################
class TasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Tasks
        fields = ('id','name','description','date','status')
###########################################################################################
class UserSchema(ma.SQLAlchemyAutoSchema):
    #Nested(RoleSchema, many=True)
    tasks=ma.Nested(TasksSchema(), many=True)
    class Meta:
        
        model=User
        #fields = ('id', 'username', 'first_name', 'last_name','email','pictures','contacts')
        fields = ('id', 'first_name','middle_name' ,'last_name','email','date_registerd','tasks')

#################################################################################################
class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Admin
        fields = ('id', 'first_name','middle_name', 'last_name','username')
#################################################################################################

#################################################################################################
#################################################################################################
