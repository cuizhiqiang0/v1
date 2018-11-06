#admin.py
from flask import Blueprint,render_template, request, redirect
from app import db
from .models import Admin

admin = Blueprint('admin',__name__)

@admin.route('/index')
def index():
    return render_template('admin/index.html')

@admin.route('/add/',methods=['POST','GET'])
def add():
    if request.method == 'POST':
        p_admin = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)

        if not p_admin or not p_email or not p_password:
            return 'input error'

        newobj = Admin(nickName=p_admin, email=p_email, password=p_password)
        db.session.add(newobj)
        db.session.commit()
        admins = Admin.query.all()
        return render_template('admin/add.html',admins=admins)
    admins = Admin.query.all()
    return render_template('admin/add.html',admins=admins)

@admin.route('/show')
def show():
    return 'admin_show'