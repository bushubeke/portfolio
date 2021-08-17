from flask import Flask,current_app, request, session,render_template
import os 
from .config import ProductionConfig
from .models import db
from .models.todo_models import *

from .fileresponse.front import front,login_manager


#print()
# this is the application factory
def create_prod_app():
    app = Flask(__name__)
    print(' * currently running with production configuration')
    app.config.from_object(ProductionConfig)
    
    
    

    db.init_app(app)
    
    ma.init_app(app)
    

    login_manager.init_app(app)
    
    app.app_context().push()
    app.register_blueprint(front,url_prefix='/')   
            

    @app.errorhandler(404)
    def not_found(e):
            title="Error "
            
            return render_template("error.html",title=title)
    return app