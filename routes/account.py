
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from forms.login import LoginForm, ChangePassForm, ChangePassAdminForm, RegisterForm, AddRoleForm, AddUserToRoleForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from model.user import User
from model.role import Role
from controllers.account import AccountController

account_api = Blueprint('account_api', __name__)
controller = AccountController()

@account_api.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('organization_api.all'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_byname(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('account_api.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('organization_api.all')
        return redirect(next_page)
    return render_template('accounts/login.html', form=form)


@account_api.route('/changepass', methods=['GET', 'POST'])
@login_required
def changepass():
    form = ChangePassForm()
    message = ''
    if form.validate_on_submit():
        user = current_user
        if not user.check_password(form.current_password.data):
            form.current_password.errors.append('Your password is incorrect')
        else:
            user.set_password(form.new_password.data)
            message = 'Password change is successful'
    return render_template('accounts/changepass.html', form=form, message=message)


@account_api.route('/changepass/admin', methods=['GET', 'POST'])
@login_required
def changepass_admin():
    form = ChangePassAdminForm()
    message = ''
    if form.validate_on_submit():
        user = User.find_byname(form.target_username.data)
        if user is None:
            form.target_username.errors.append('User not found')
        else:
            if not current_user.check_password(form.current_password.data):
                form.current_password.errors.append('Your password is incorrect')
            else:
                user.set_password(form.new_password.data)
                message = 'Password change is successful'
    return render_template('accounts/changepass_admin.html', form=form, message=message)


@account_api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.find_byname(form.username.data)
        if user is not None:
            form.username.errors.append('Username is already taken')
        else:
            user = User.add(form.username.data, form.password.data)
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('organization_api.all'))
    return render_template('accounts/register.html', form=form)


@account_api.route('/resetadmin')
def reset_admin():
    user = User.find(1)
    user.set_password('test123')
    return redirect(url_for('account_api.login'))


@account_api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('account_api.login'))


@account_api.route('/add_to_role', methods=['GET', 'POST'])
@login_required
def add_to_role():
    form = AddUserToRoleForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            form.current_password.errors.append('Your password is incorrect')
        else:
            user = User.find_byname(form.target_username.data)
            if user is None:
                form.target_username.errors.append('Specified username does not exist')
            role = Role.find_byname(form.role_name.data)
            if role is None:
                form.role_name.errors.append('Specified role does not exist')
            if user is not None and role is not None:
                if not form.remove_instead.data:
                    user.add_to_role(role_name=form.role_name.data)
                else:
                    user.remove_from_role(role_name=form.role_name.data)
    return render_template('accounts/addusertorole.html', form=form)


@account_api.route('/add_role', methods=['GET', 'POST'])
@login_required
def add_role():
    form = AddRoleForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            form.current_password.errors.append('Your password is incorrect')
        else:
            role = Role.find_byname(form.role_name.data)
            if role is not None:
                form.role_name.errors.append('this role already exists')
            else:
                Role.add(form.role_name.data)
    return render_template('accounts/addrole.html', form=form)


@account_api.route('/add_to_role/<user_name>/<role_name>')
def add_to_role_api(user_name, role_name):
    user = User.find_byname(user_name)
    if user is not None:
        user.add_to_role(role_name=role_name)
    return ''


@account_api.route('/remove_from_role/<user_name>/<role_name>')
def remove_from_role_api(user_name, role_name):
    user = User.find_byname(user_name)
    if user is not None:
        user.remove_from_role(role_name=role_name)
    return ''


@account_api.route('/add_role/<role_name>')
def add_role_api(role_name):
    Role.add(role_name)
    return ''


@account_api.route('/search_users/<query>/<resource>')
def search_user(query, resource):
    return jsonify(controller.user_search(query, resource))


@account_api.route('/save_roles', methods=['POST'])
def save_roles():
    return jsonify(controller.save_roles(request.json))