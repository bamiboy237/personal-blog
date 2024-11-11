from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import User
from datetime import datetime, timezone

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class PostForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired(), 
                                    Length(max=140, message="Title must be 140 characters or fewer.")])
    content = TextAreaField('Content', 
                            validators=[DataRequired(message="Content cannot be empty.")])
    submit = SubmitField('Add Post')

class SettingsForm(FlaskForm):
    site_name = StringField('Site Name', validators=[DataRequired()])
    maintenance_mode = BooleanField('Maintenance Mode')
    submit = SubmitField('Save Settings')