from flask import Blueprint,render_template,redirect,request
from app import  db
from .models import User,Post

user = Blueprint('user', __name__)

@user.route('/index')
def index():
    return render_template('user/index.html')

@user.route('/add/', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        p_user = request.form.get('username', None)
        p_email = request.form.get('email', None)
        p_password = request.form.get('password', None)

        if not p_user or not p_email or not p_password:
            return 'input error'

        newobj = User(nickName = p_user, email=p_email, password=p_password)
        db.session.add(newobj)
        db.session.commit()
        users = User.query.all()
        return render_template('user/add.html', users=users)
    users = User.query.all()
    return render_template('user/add.html', users=users)

@user.route('/show')
def show():
    return 'user_show'