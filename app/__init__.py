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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:apexdgreat@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://czfzleixetfgcr:b82cad327ed9cd7be904d0e54f70ea60e307b0b458ae83e2f6c5b1b37d11a5a3@ec2-34-200-205-45.compute-1.amazonaws.com:5432/da7okhkih9p37o'
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