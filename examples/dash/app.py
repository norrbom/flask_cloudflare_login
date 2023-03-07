from os import getenv
from config import is_enabled, load_config
from auth import User, AnonymousUser
from auth import group_required
import functions as fn
import logger
import logging
import json
from flask import Flask, request, abort, jsonify
from flask import Response
from flask_login import logout_user, current_user, LoginManager
from flask_cloudflare.cache import cache
from flask_cloudflare import access
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# load dot env config
dot_env = load_config()

# configure flask
server = Flask(getenv('APP_NAME'))
server.config.update(
    TESTING=is_enabled('TESTING'),
    DEBUG=is_enabled('DEBUG'),
    SECRET_KEY=getenv('SECRET_KEY')
)

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.anonymous_user = AnonymousUser

# configure cache
cache.init_app(server)


# Flask routes
@server.route('/healthz/live')
@group_required(
    groups=['group_admin'], fail_response=Response('Unauthorized!', status=401)
    )
def healthz():
    return jsonify({"status": 200})


# Callback method for Flask to load user object using request object
@login_manager.request_loader
def load_user_from_request(request):
    token = access.get_token(request)
    if token:
        log.info("Loading user from request using token")
        payload = access.get_payload(token)
        if payload:
            groups = access.get_groups(
                token=token,
                group_filter=getenv('GROUP_FILTER')
                )
            email = payload.get('email')
            if email:
                log.debug('creating user')
                return User(email, groups)
    # create user from test config
    else:
        if getenv('TEST_CF_EMAIL') and getenv('TEST_CF_GROUPS'):
            return User(
                getenv('TEST_CF_EMAIL'),
                json.loads(getenv('TEST_CF_GROUPS'))
                )
    return None


# configure Dash
app = dash.Dash(
    getenv('APP_NAME'),
    server=server,
    use_pages=True,
    suppress_callback_exceptions=True,
    url_base_pathname=getenv('BASE_PATH', '/'),
    title=getenv('APP_NAME'),
    external_stylesheets=[dbc.themes.FLATLY]
    )

# get logger
log = logging.getLogger(getenv('APP_NAME'))

# setup Dash layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        html.Div(id='page-content'),
        dash.page_container
    ]
)


# Dash callbacks
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def top_menu_router(input_value):
    if input_value == getenv('BASE_PATH') + 'logout':
        if current_user.is_authenticated:
            log.info('logging out user and clearing cache')
            access.clear_cache(
                access.get_token(request),
                group_filter=getenv('GROUP_FILTER', None)
                )
            logout_user()
    return [
        dbc.Nav([
            dbc.NavLink("Home", href=getenv('BASE_PATH')),
            dbc.NavLink("Logout", href="./logout"),
            dbc.NavLink("Me", href="./profile"),
            dbc.NavLink("Restricted", href="./restricted")
        ])
    ]


# App is running with Flask without wsgi
if __name__ == '__main__':
    logger.configure_logging()
    # application config at startup
    log.info(fn.app_config(dot_env))
    # start Flask
    app.run_server(
        port=5000,
        debug=is_enabled('DEBUG')
        )

# App is running with Gunicorn wsgi server
if __name__ != '__main__':
    # configure logging
    logger.configure_logging()
    # application config at startup
    log.info(fn.app_config(dot_env))
