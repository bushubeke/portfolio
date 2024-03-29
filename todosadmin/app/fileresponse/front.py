import re
from flask import Blueprint, render_template, abort,session,url_for,g,redirect,request
from jinja2 import TemplateNotFound
from passlib.hash import pbkdf2_sha512
from ..forms.model_forms import * 
from .. models.todo_models import *
import copy
from flask_login import login_manager, login_user,logout_user,login_required,current_user,LoginManager

front = Blueprint('front', __name__,
                        template_folder='templates')
###############################################################
#global variable to track login_status of user here
login_manager=LoginManager()  
@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email).first()

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('front.login'))    
 
@front.route('/',methods=["GET"])
def index():
    title="HomePage"
    if not current_user.is_authenticated:
       cuvalue=None
    try:
        return render_template('index.html',title=title)
    except TemplateNotFound:
        abort(404)

@front.route('/login',methods=["GET","POST"])
def login():
    title="LOGIN PAGE"
    login_form=LoginForm()
    if not current_user.is_authenticated:
        if request.method == "GET":
            try:
                return render_template('login.html',login_form=login_form)
            except TemplateNotFound:
                abort(404)
        elif request.method == "POST":
            if login_form.validate():
                user=User.query.filter_by(email=login_form.data['email']).first()
                #the if condtional below also verifys password
                if user and pbkdf2_sha512.verify(login_form.data['password'],user.password):
                    login_user(user,remember=True)
                    return render_template('index.html',title="Homepage")
                return redirect(url_for('front.login'))
            return redirect(url_for('front.login'))
        else:
            return render_template('index.html',title="Homepage")
    return redirect(url_for('front.index')) 
         
@front.route('/logout',methods=["GET"])
def logout():
    try:
       logout_user()
    except:
        pass
    finally:
        return redirect(url_for('front.login'))


@front.route('/register',methods=["GET","POST"])
def register():
    register_form=RegisterForm()
    if request.method == "GET":
        try:
            return render_template('register.html',register_form=register_form)
        except TemplateNotFound:
            abort(404)
    elif request.method == "POST":
        if register_form.validate_on_submit():
            try:
                if User.query.filter_by(email=register_form.data['email']).first() is None:    
                    mod_data=copy.deepcopy(register_form.data)
                    mod_data.pop('confirm')
                    mod_data.pop('csrf_token')
                    user=User(**mod_data)
                    #this is using sha512 from passlib function
                    user.password=pbkdf2_sha512.using(rounds=25000,salt_size=80).hash(mod_data['password'])
                    db.session.add(user)
                    db.session.commit()
                    return render_template('index.html',title="Homepage")
                else:
                    return render_template('register.html',register_form=register_form,)
            except:
                db.session.rollback()
            finally:
                db.session.close()
        return render_template('register.html',register_form=register_form)


@front.route("/about",methods=["GET"])
def about_page():
    title="About Page"    
    return render_template('about.html',title=title)
######################################################################
# this is the tasks page 
# this genrally won't be accessed unless logged in
#######################################################################
@front.route('/tasks',methods=["GET","POST"])
#@login_required
def tasks():
    title="Tasks"
    """ 
    please note that this section is does not perform curd operations on tasks tabel yet
    """   
    tasks_form=TasksForm()
    if request.method == "GET":
        tasks_v=Tasks.query.filter_by(user=current_user.id).all()
        task_mash=TasksSchema(many=True)
        tasks=task_mash.dump(tasks_v)
        update_forms=[]
        for x in tasks:
            format_str = '%Y/%m/%d'
            datestr="/".join(x["date"][:-9].split("-"))
            x["date"]=datetime.datetime.strptime(datestr,format_str).date()
            update=TasksFormNot(**x)     
            update_forms.append(update)
        return render_template('tasks.html',title=title,tasks=zip(tasks,update_forms),tasks_form=tasks_form)
    elif request.method == "POST":
        if tasks_form.validate():
            try:
                    mod_data=copy.deepcopy(tasks_form.data)
                    mod_data.pop('csrf_token')
                    task=Tasks(**mod_data)
                    current_user.tasks.append(task)
                    db.session.commit()
            except Exception as e:
                print(f"### is {e}")
                db.session.rollback()
            finally:
                db.session.close()
        return redirect(url_for('front.tasks'))
    else:
        return render_template('index.html',title=title)
    
######################################################################
#task update and delete section
#######################################################################
@front.route('/tasksup',methods=["POST"])
@login_required
def update_task():
        title="Tasks"
        tasks_formnot=TasksFormNot()        
        try:
            taskup=Tasks.query.filter_by(id=int(tasks_formnot.data["id"]))
            
            upd_data=copy.deepcopy(tasks_formnot.data)
            upd_data.pop('id')
            taskup.update(upd_data)
            db.session.commit()
        except Exception as e:
             print(f"### is {e}")
             db.session.rollback()
        finally:
             db.session.close()
        return redirect(url_for('front.tasks'))
@front.route('/tasksdel',methods=["POST"])
@login_required
def delete_task():
        title="Tasks"
        try:
            Tasks.query.filter_by(id=int(request.form.to_dict()["id"])).delete()
            db.session.commit()
        except Exception as e:
             print(f"### is {e}")
             db.session.rollback()
        finally:
             db.session.close() 
        return redirect(url_for('front.tasks'))
#

######################################################################
# this is about page route
#######################################################################
@front.route("/profile",methods=["GET"])
@login_required
def profile_page():
        title="Profile"
        puser_user=User.query.filter_by(email=current_user.email).first()
        user_stat={}
        user_stat["num_of_tasks"]=len(puser_user.tasks)
        user_stat["num_of_ongoing"]=len([x for x in puser_user.tasks if x.status=="ongoing" ])
        user_stat["num_of_closed"]=len([x for x in puser_user.tasks if x.status=="closed" ])
        return render_template('profile.html',title=title,user_stat=user_stat)
   
######################################################################
# this is  adminpage
#######################################################################
@front.route("/admin",methods=["GET","POST"] )
def admin_login():
    title="ADMIN LOGIN"
    login_form=AdminForm()
    current_user=None
    login_status=False
    if 'username' in session:
            login_status=True
            current_user=Admin.query.filter_by(username=session['username']).first()
    if request.method == "GET":
        if  login_status:
            return redirect(url_for("front.admin_dash"))
        return render_template("admin.html",title=title,login_form=login_form,current_user=current_user)
    elif request.method == "POST":
        # #################################################################
         if login_form.validate():
            user=Admin.query.filter_by(username=login_form.data['username']).first()
            #the if condtional below also verifys password
           
            if user and pbkdf2_sha512.verify(login_form.data['password'],user.password):
                session['username'] = login_form.data['username']
                return redirect(url_for("front.admin_dash"))
            return redirect(url_for("front.admin_login"))
         return redirect(url_for("front.admin_login"))
        
    else:
       return render_template('index.html',title="Homepage",current_user=current_user) 
######################################################################
# this is dashboard route test page page route
#######################################################################
@front.route('/admin/dashboard')
def admin_dash():
    if 'username' in session:
        login_status=True
        admin_user=Admin.query.filter_by(username=session['username']).first()
        users_v=User.query.all()
        ussc=UserSchema(many=True)
        usscp=ussc.dump(users_v)
        simple_stats={}
        simple_stats["number_of_users"]=len(users_v)
        simple_stats["number_of_tasks"]=len(Tasks.query.all())
        return render_template('dashboard.html',title="Admin Board",login_status=login_status,admin_user=admin_user,usscp=usscp,simple_stats=simple_stats)
    return redirect(url_for("front.admin_login"))

######################################################################
# this is dashboard route test page page route
#######################################################################
@front.route('/admin/dashdelete',methods=["POST"])
def delete_dash():
    if 'username' in session and request.method == "POST":
        login_status=True
        admin_user=Admin.query.filter_by(username=session['username']).first()
        try:
            user_to_delete=User.query.filter_by(id=int(request.form.to_dict()["id"])).delete()
            db.session.query(Tasks).filter(Tasks.user==int(request.form.to_dict()["id"])).delete()
            db.session.commit()
        except Exception as e:
             print(f"### is {e}")
             db.session.rollback()
        finally:
             db.session.close() 
        return redirect(url_for("front.admin_dash"))
    return redirect(url_for("front.admin_login"))
######################################################################
# this is admin logout route test page page route
#######################################################################
@front.route('/admin/logout')
def admin_logout():
    try:
       session.pop('username', None)
    except:
        pass
    finally:
        return redirect(url_for('front.admin_login'))
    

######################################################################
# this is Markdown previewr route using markdown previewr
#######################################################################

@front.route('/markdown')
def markdown():
      title="Markdown Previewer"
      return render_template('marked.html',title=title)
    
######################################################################
# this is tails test page page route
#######################################################################

@front.route("/tail",methods=["GET"])
def tail_page():

    return render_template('tail.html')


