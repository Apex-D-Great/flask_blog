from importlib.resources import contents
import profile
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.model import User
from flask_wtf.file import FileField

class Login(FlaskForm):
    email = StringField(label="Email" , validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label="submit")


class Register(FlaskForm):
    def validate_name(self, user_to_check):
        user = User.query.filter_by(name=user_to_check.data).first()
        if user:
            raise ValidationError("username already exist, try another username")
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("email already exist, try another email")
    name = StringField(label="Name" , validators=[DataRequired()])
    email = StringField(label="Email" , validators=[DataRequired()])
    password1 = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField(label="Submit")

class Form(FlaskForm):
    name = StringField(label="enter your name" , validators=[DataRequired()])
    submit = SubmitField(label="submit")  

class DashForm(FlaskForm):
    name = StringField(label="Name" , validators=[DataRequired()])
    email = StringField(label="Email" , validators=[DataRequired()])
    # profile_pic = FileField('Profile Pic')
    about = StringField(label="About", widget=TextArea())
    submit = SubmitField(label="submit")  

class SearchForm(FlaskForm):
    searched = StringField(label="searched" , validators=[DataRequired()])
    submit = SubmitField(label="submit") 

class AdminForm(FlaskForm):
    adminsearch = StringField(label="adminsearch" , validators=[DataRequired()])
    submit = SubmitField(label="submit")  

class PostForm(FlaskForm):
    title = StringField(label="Title" , validators=[DataRequired()])
    # author = StringField(label="Author")
    slug = StringField(label="Slug", validators=[DataRequired()])
    # content = StringField(label="Content" , validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField(label="submit")