from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

#登录机制不是采取的用户名，密码，而是openid，后面可以采用用户名，密码，数据库
class LoginForm(Form):
    userName = StringField('userName', validators=[DataRequired()])
    passWord = StringField('passWord', validators=[DataRequired()])
    remember_me = BooleanField('remrember_me', default=False)