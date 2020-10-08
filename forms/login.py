from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ChangePassForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')


class ChangePassAdminForm(FlaskForm):
    current_password = PasswordField('Your Password', validators=[DataRequired()])
    target_username = StringField('Username of target account', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

class AddRoleForm(FlaskForm):
    current_password = PasswordField('Your Password', validators=[DataRequired()])
    role_name = StringField('Role Name', validators=[DataRequired()])
    submit = SubmitField('Add Role')

class AddUserToRoleForm(FlaskForm):
    current_password = PasswordField('Your Password', validators=[DataRequired()])
    target_username = StringField('Username of target account', validators=[DataRequired()])
    role_name = StringField('Role Name', validators=[DataRequired()])
    remove_instead = BooleanField('Remove from role')
    submit = SubmitField('Add User to Role')