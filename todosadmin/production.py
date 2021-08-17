import os
from flask_migrate import Migrate
from app import create_prod_app,db
basde=os.path.abspath(os.path.dirname(__file__))


MIGRATION_DIR = os.path.join(basde, 'prodmigrations')
app=create_prod_app()
migrate_prod = Migrate(app, db, directory=MIGRATION_DIR)
    

if __name__ == "__main__":
     app.run(host='0.0.0.0',port="8000")


#########################################################################

#plsease read the multiline comment below before runing and testing the progress

###########################################################################
""""
the app normally runs on port 1000


also install the req.txt reqirments file before running

pip install -rU req.txt

######################################################
normally flask extenstions were used for serialization
and model building

the main extenstions were
Flask-Migrations(#to migrate my models)
Flask-WTF
Flask-sqlalchemy
Flask-marshmallow
marshmallow-sqlalchemy (#which is going to be used for serialzing the task)

#############################################################

i normally used the template from my github repository to structure this project
some unwanted moduels have been removed as well
 https://github.com/bushubeke/python-compose/tree/main/nginix%2Bgunicorn%2Bflask
######################################################

to use gunicorn run the command below in folder where production.py is found

gunicorn production:app -b 0.0.0.0

or 

python production.py

###################################################

finally, you can check out the login and login functionality by testing the /tasks page 
also (the login will be changed to Logout if logged in ) and signup registery works as well
note that the password is stored in hashed form using sha512 (from passlib)

the /tasks page does update/add and delete entry as well as rendering which is the addition in this version of todos 2

and not tests were written  here as well the route

the routes are found in "app/fileresponse" module
the models are found in "app/models" module
the forms are found in "app/forms" module 


"""
