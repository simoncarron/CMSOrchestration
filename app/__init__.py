from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_ldap3_login import LDAP3LoginManager

import app.module.mod_database as database

import app.module.mod_cms as cms

import config as setting

def create_app():
    a = cms.Acano(setting.CMS_IP_ADDRESS + ":" + setting.CMS_PORT, setting.CMS_USERNAME, setting.CMS_PASSWORD)

    ldapServers = a.get_ldap_servers()
    ldapSources = a.get_ldap_sources()

    print(ldapServers)
    print(ldapSources)

    app = Flask(__name__)

    # Hostname of your LDAP Server
    app.config['LDAP_HOST'] = ldapServers["ldapServers"]["ldapServer"][0]['address']+":"+ldapServers["ldapServers"]["ldapServer"][0]['portNumber']

    # The Username to bind to LDAP with
    app.config['LDAP_BIND_USER_DN'] = ldapServers["ldapServers"]["ldapServer"][0]['username']

    # The Password to bind to LDAP with
    app.config['LDAP_BIND_USER_PASSWORD'] = setting.LDAP_PASSWORD

    # Base DN of your directory
    app.config['LDAP_BASE_DN'] = ldapSources["ldapSources"]["ldapSource"][0]['baseDn']

    # The RDN attribute for your user schema on LDAP
    app.config['LDAP_USER_RDN_ATTR'] = 'cn'

    # The Attribute you want users to authenticate to LDAP with.
    app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'

    app.config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'

    app.config['SECRET_KEY'] = 'thisisthesecretkey'

    app.config['DEBUG'] = True

    users = {}

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    ldap_manager = LDAP3LoginManager(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        if id in users:
            return users[id]
        return None

    @ldap_manager.save_user
    def save_user(dn, username, data, memberships):
        user = User(dn, username, data)
        users[dn] = user
        return user

    from .views.admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .views.home import home
    app.register_blueprint(home, url_prefix='/')

    from .views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app