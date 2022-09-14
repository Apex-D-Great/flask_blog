from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:apexdgreat@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
# cke editor(rich editor)
ckeditor = CKEditor(app)
migrate = Migrate(app, db)
bycrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from app import route

if __name__ == "__main__":
    app.run()