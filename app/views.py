from app import app,logger,login_manager,db
from flask import render_template,flash,redirect,request,make_response,jsonify,url_for,g,session,escape
import flask_login
from flask_login import login_user,logout_user,current_user
import random
import time
from datetime import datetime
from .forms import LoginForm,EditForm
from .admin import admin
from .user import user
from .models import User

app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    logger.warning("index page method is <%s>", request.method)
    logger.warning('cookie name <%s>' % request.cookies.get('nickName'))

    if 'username' in session:
        logger.warning("login user is %s" % flask_login.current_user )
        logger.warning('Logged in as %s' % escape(session['nickName']))
        return render_template('index.html', name=session['nickName'])
    else:
        logger.warning("you are not logged in")
        #return render_template('login.html')
        return redirect(url_for('login'))
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
        logger.warning("login method post!")
        username = request.form['username']
        password = request.form['password']
        logger.warning("username:<%s>, password<%s>" %(username,password))

        user = User.query.filter_by(nickName = username, password = password).first()
        if user != None:
            # set login user
            #user = User(nickName=username, password=password)
            flask_login.login_user(user)

            g.user = user
            logger.warning(g.user.is_authenticated)
            resp = make_response(render_template('index.html', name=username))
            resp.set_cookie('username', username)

            #return jsonify({'status': '0',  'errmsg': '登录成功！'})
            return render_template('index.html')
        else:
            #return abort(401)
            return jsonify({'status': '-1', 'errmsg': '用户名或密码错误！'})

    logger.warning("login get method")
    return render_template('login.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    logger.debug('log out page')
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/api', methods=['GET'])
@flask_login.login_required
def api():
    return jsonify({'value':random.random(), 'timestamp':int(time.time())})

@login_manager.request_loader
def request_loader(req):
    logger.warning('request_loader url is %s, request args is %s' % (req.url, req.args))
    authorization = request.headers.get('Authorization')
    logger.warning('Authorization is %s' % authorization)
    #模拟api登录
    if authorization:
        user = User()
        user.nickName = 'admin'
        logger.warning('user is <%s>' % user)
        return user
    return None

@app.route('/error')
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(500)
def error(e):
    logger.warning('error occured: <%s>' % e)
    try:
        code = e.code
        if code == 400:
            return render_template('400.html')
        elif code == 401:
            return render_template('401.html')
        else:
            return render_template('error.html')
    except Exception as e:
        logger.warning('exception is <%s>' % e)
    finally:
        return render_template('error.html')

@app.route('/user/<nickName>')
@flask_login.login_required
def user(nickName):
    logger.warning('/user<nickname<%s>>' % nickName)
    user = User.query.filter_by(nickName= nickName).first()
    if user == None:
        flash('user' + nickName + 'not found')
        return redirect(url_for('index'))
    posts = [
        {'author' : user, 'body' : 'Test post #1'},
        {'author' : user, 'body' : 'Test post #2'}
    ]
    return render_template('user.html', user = user, posts = posts)

@app.route('/edit', methods=['GET', 'POST'])
@flask_login.login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickName = form.nickName.data
        g.user.about_me = form.about_me.data

        db.session.add(g.user)
        db.session.commit()
        flash('your changes have been saved')
        return redirect(url_for('edit'))
    else:
        form.nickName.data = g.user.nickName
        form.about_me.data = g.user.about_me

    return  render_template('edit.html', form=form)

@app.route('/follow/<nickName>')
@flask_login.login_required
def follow(nickName):
    user = User.query.filter_by(nickName=nickName).first()
    if user is None:
        flash('user <%s> not found' % nickName)
        return redirect(url_for('index.html'))
    if user == g.user:
        return  redirect(url_for('user', nickName=nickName))

    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickName + '!')
        return redirect(url_for('user', nickName=nickName))

    db.session.add(u)
    db.session.commit()
    flash('%s is follow %s', (g.user.nickName, nickName))
    return redirect(url_for('user', nickName=nickName))

@app.route('/unfollow/<nickName>')
@flask_login.login_required
def unfollow(nickName):
    user = User.query.filter_by(nickName=nickName).first()
    if user is None:
        flash('user <%s> not found' % nickName)
        return redirect(url_for('index.html*
    if user == g.user:
        return redirect(url_for('user', nickName=nickName))

    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot follow ' + nickName + '!')
        return redirect(url_for('user', nickName=nickName))

    db.session.add(u)
    db.session.commit()
    flash('%s stop following %s', (g.user.nickName, nickName))
    return redirect(url_for('user', nickName=nickName))