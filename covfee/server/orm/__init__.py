import os
from urllib.parse import urlparse

from .db import db
from .hit import *
from .project import *
from .task import *
from .user import *


def load_config(app, mode, host=None):
    app.config['COVFEE_ENV'] = mode
    # load the base configuration object
    app.config.from_object('covfee.server.config')

    # update with the custom project config files
    if mode == 'local':
        app.config.from_pyfile(os.path.join(
            os.getcwd(), 'covfee.local.config.py'), silent=True)
    elif mode == 'dev':
        app.config.from_pyfile(os.path.join(
            os.getcwd(), 'covfee.development.config.py'), silent=True)
    elif mode == 'deploy':
        app.config.from_pyfile(os.path.join(
            os.getcwd(), 'covfee.deployment.config.py'), silent=True)
    else:
        raise Exception(f'Unrecognized application mode {mode}.')

    # check if SSL enabled
    app.config['SSL_ENABLED'] = ('SSL_KEY_FILE' in app.config and 'SSL_CERT_FILE' in app.config)

    protocol = 'https' if app.config['SSL_ENABLED'] else 'http'
    host = host if host is not None else '127.0.0.1'

    # URL that will be used to access the app
    app.config['BASE_URL'] = f'{protocol}://{host}:5000'
    
    # URL of the webpack hot bundle
    app.config['DEV_BUNDLE_URL'] = f'{protocol}://{host}:8085'
        
    # apply extended config
    app_path = urlparse(app.config['BASE_URL']).path
    if app_path == '':
        app_path = '/'

    app.config.update(
        # copy over secret key
        JWT_SECRET_KEY=app.config['COVFEE_SECRET_KEY'],

        # create sqlalchemy database uri
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.config["DATABASE_PATH"]}',

        # create derived URLs
        PROJECT_WWW_URL=app.config['BASE_URL'] + '/www',
        BUNDLE_URL=app.config['BASE_URL'] + '/www',
        APP_URL=app.config['BASE_URL'] + '/#',
        ADMIN_URL=app.config['BASE_URL'] + '/admin#',
        LOGIN_URL=app.config['BASE_URL'] + '#login',
        API_URL=app.config['BASE_URL'] + '/api',
        AUTH_URL=app.config['BASE_URL'] + '/auth',
        # Set the cookie paths, so that you are only sending your access token
        # cookie to the access endpoints, and only sending your refresh token
        # to the refresh endpoint. Technically this is optional, but it is in
        # your best interest to not send additional cookies in the request if
        # they aren't needed.
        JWT_ACCESS_COOKIE_PATH=app_path,
        JWT_REFRESH_COOKIE_PATH=os.path.join(app_path, 'auth/refresh')
    )

    # point to webpack-dev-server bundles in dev mode
    if mode == 'dev':
        app.config['BUNDLE_URL'] = app.config['DEV_BUNDLE_URL']

    # create the frontend config object:
    app.config['FRONTEND_CONFIG'] = {
        # frontend only has two environments: production and development
        'env': 'production' if mode in ['local', 'deploy'] else 'development',
        'socketio_enabled': app.config['SOCKETIO_ENABLED'],
        'www_url': app.config['PROJECT_WWW_URL'],
        'app_url': app.config['APP_URL'],
        'admin_url': app.config['ADMIN_URL'],
        'base_url': app.config['BASE_URL'],
        'api_url': app.config['API_URL'],
        'auth_url': app.config['AUTH_URL'],
    }
