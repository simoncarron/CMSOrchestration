
from flask import Blueprint, render_template, redirect, url_for, request, flash, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_ldap3_login.forms import LDAPLoginForm

from ..models import User

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LDAPLoginForm()

    if form.validate_on_submit():

        login_user(form.user)

        return redirect('/')

    return render_template('auth/index.html', title='Sign In', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
