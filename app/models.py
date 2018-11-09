from app import db
import flask_login
from hashlib import md5
from app import login_manager

@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except ValueError:
        return None

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    nickName = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(40), index = True, unique = True)
    password = db.Column(db.String(32), index = True, unique=False)
    posts = db.relationship('Post', backref='author',lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickName)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar' + md5(self.email.encode('utf8')).hexdigest() + '?d=mm&s=' + str(size)

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

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self




class Post(db.Model):
    __tablename__  = 'post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %(self.body)

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    nickName = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=False)

    #posts = db.relationship('Post', backref='author',lazy='dynamic')

    def __repr__(self):
        return '<Admin %r>' % (self.nickName)
