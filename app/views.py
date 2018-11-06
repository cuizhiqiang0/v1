from app import app,logger
from flask import render_template,flash,redirect,request,make_response,jsonify
import flask_login
from .forms import LoginForm
from .admin import admin
from .user import user
from .models import User

app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')


@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    logger.debug("index page method is <%s>", request.method)
    user = {'username': 'cui'}
    posts = [
        {
            'author': {'username' : 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for 用户名="' + form.userName.data  + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form = form)
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        logger.debug("login method post!")
        username = request.form['username']
        password = request.form['password']
        logger.debug("username:<%s>, password<%s>" %(username,password))

        if password == 'admin123' and username == 'admin':
            # set login user
            user = User(nickName=username, password=password)

            flask_login.login_user(user)

            resp = make_response(render_template('index.html', name=username))
            resp.set_cookie('username', username)

            #return jsonify({'status': '0', 'errmsg': '登录成功！'})
            return render_template('index.html')
        else:
            #return abort(401)
            return jsonify({'status': '-1', 'errmsg': '用户名或密码错误！'})

    logger.debug("login get method")
    return render_template('login.html')

@app.route('/logout')