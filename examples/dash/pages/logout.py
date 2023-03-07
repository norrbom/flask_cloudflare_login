from os import getenv
import dash
from dash import html
from auth import login_required

dash.register_page(__name__, path='/logout', title=f"{getenv('APP_NAME')} - Logout")


@login_required
def layout():
    return html.Div(children=[
        html.H1(
            children='Logout'
        )
    ])