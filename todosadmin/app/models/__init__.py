import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from ..config import key

from flask_login import UserMixin

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer,String, ForeignKey
from passlib.hash import pbkdf2_sha512

db = SQLAlchemy(session_options={'autocommit': False})
ma=Marshmallow()