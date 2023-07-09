from os import getenv
import dash
from dash import html

dash.register_page(__name__, path="/", title=f"{getenv('APP_NAME')} - Home")


def layout():
    return html.Div(children=[html.H1(children="Home")])
