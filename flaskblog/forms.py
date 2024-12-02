from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    #custom validators to check if username and email already taken
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Use a different one.')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken. Use a different one.')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    # user to stay login for sometime after their browser closes using a secure 
    # we need to set up a secret key, it protects against modifying cookies and cross site request forgery 
    
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    #custom validators to check if username and email already taken
    def validate_username(self,username):
        if username.data != current_user.username: #if the new username is different from existing one in the database then we will proceed
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken. Use a different one.')
        
    def validate_email(self,email):
        if email.data != current_user.email: #if the new email is different from existing one in the database then we will proceed
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken. Use a different one.')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')