import os
from app import app

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))
#数据库可以采用sql3 ， 也可以mysql
#数据库文件路径
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:cuicui@localhost/flask_micblog"
SQLALCHEMY_TRACK_MODIFICATIONS = True
#数据库迁移文件路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_respository')
