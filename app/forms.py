from flask_wtf import Form
from wtforms import StringField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length
from .models import User

#登录机制不是采取的用户名，密码，而是openid，后面可以采用用户名，密码，数据库
class LoginForm(Form):
    userName = StringField('userName', validators=[DataRequired()])
    passWord = StringField('passWord', validators=[DataRequired()])
    remember_me = BooleanField('remrember_me', default=False)

class EditForm(Form):
    nickName = StringField('nickName', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    '''
    def __init__(self, orignal_nickName, *args, **kwargs):
        Form.__init__(self, * args, **kwargs)
        self.original_nickName = orignal_nickName

    def validate(self):
        if not Form.validate():
            return False
        if self.nickName.data == self.original_nickName:
            return True
        user = User.query.filter_by(nickName = self.nickName.data)
        if user != None:
            self.nickName.errors.append()
    '''
