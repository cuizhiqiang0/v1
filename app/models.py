from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickName = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref='author',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickName)

    @property
    def is

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %(self.body)