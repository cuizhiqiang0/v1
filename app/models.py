from app import db
import flask_login

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    nickName = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(40), index = True, unique = True)
    password = db.Column(db.String(32), index = True, unique=False)
    #posts = db.relationship('Post', backref='author',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickName)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

class Post(db.Model):
    __tablename__  = 'post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.column(db.DateTime)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %(self.body)

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    nickName = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=False)

    # posts = db.relationship('Post', backref='author',lazy='dynamic')

    def __repr__(self):
        return '<Admin %r>' % (self.nickName)
