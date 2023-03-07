from os import getenv
import dash
from dash import html
from auth import group_required

dash.register_page(
    __name__, path='/restricted', title=f"{getenv('APP_NAME')} - Restricted"
    )


@group_required(groups=['group_admin'])
def layout():
    return html.Div(children=[
        html.H1(
            children='Restricted'
        )
    ])
