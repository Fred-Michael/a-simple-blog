from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
   remember = BooleanField('Remember Me')
   submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
   name = StringField('Name', validators=[DataRequired()])
   username = StringField('Username', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired(), Email()])
   password = PasswordField('Password', validators=[DataRequired()])
   password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Sign Up')

   def validate_username(self, username):
      user = User.query.filter_by(username = username.data).first()
      if user is not None:
         raise ValidationError("Username taken. Try another one")

   def validate_email(self, email):
      user = User.query.filter_by(email = email.data).first()
      if user is not None:
         raise ValidationError("Email address in use. Use another email address")

class CreatePostForm(FlaskForm):
   title = StringField('Article title', validators=[DataRequired()])
   content = TextAreaField('Body', validators=[Length(min=0, max=6000), DataRequired()])
   submit = SubmitField('Create Post')

class DeletePostForm(FlaskForm):
   title = StringField('Article title', validators=[DataRequired()])
   submit = SubmitField('Delete Post')

class UpdatePostForm(FlaskForm):
   title = StringField('New title', validators=[DataRequired()])
   update = TextAreaField('New Content', validators=[Length(min=0, max=7000)])
   submit = SubmitField('Update Post')

class AddCommentForm(FlaskForm):
   comment = TextAreaField('', validators=[Length(min=0, max=140)])
   submit = SubmitField('Post Comment')