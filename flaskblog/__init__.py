from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from  flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flask_restful import Api, Resource

application = Flask(__name__)
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
ma = Marshmallow(application)
api = Api(application)


#it handles all the sessions
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
application.config['MAIL_SERVER'] = 'smtp.googlemail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
application.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS')
mail = Mail(application)


from flaskblog import routes