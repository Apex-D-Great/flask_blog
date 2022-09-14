import profile
from flask_login import UserMixin
from app import db, login_manager, bycrypt
from datetime import datetime
# user table
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship("Post", backref="poster", lazy=True)
    about = db.Column(db.Text(), nullable=True)

    @property
    def password(self):
        pass
    @password.setter
    def password(self, pwd):
        self.password_hash = bycrypt.generate_password_hash(pwd).decode("utf-8")

    def check_password(self, pwd):
        return bycrypt.check_password_hash(self.password_hash, pwd)

    def __repr__(self):
        return "<name: %r>" % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    