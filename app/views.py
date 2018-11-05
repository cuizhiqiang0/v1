from app import app
from flask import render_template,flash,redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for 用户名="' + form.userName.data  + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form = form)