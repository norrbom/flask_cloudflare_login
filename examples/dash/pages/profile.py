from os import getenv
import logging
import dash
from dash import html
from flask_login import current_user
from config import is_env_value

log = logging.getLogger(getenv("APP_NAME"))
dash.register_page(__name__, path="/profile", title=f"{getenv('APP_NAME')} - Profile")


def layout():
    profile = [
        key + ": " + str(current_user.__dict__()[key])
        for key in current_user.__dict__()
    ]
    profile.append(f"is authenticated: {current_user.is_authenticated}")
    profile.append(f"is anonymous: {current_user.is_anonymous}")
    profile.append(f"is active: {current_user.is_active}")
    profile.append(f"is admin: {is_env_value('ADMINS', current_user.get_id())}")
    return html.Div(
        children=[
            html.H1(children="My Profile"),
            html.Div(
                html.Div(
                    children=[
                        html.Ul(
                            id="profile-list", children=[html.Li(p) for p in profile]
                        )
                    ],
                )
            ),
        ]
    )
