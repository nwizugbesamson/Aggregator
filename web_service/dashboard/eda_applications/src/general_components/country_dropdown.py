from dash import html, dcc
from django_plotly_dash import DjangoDash
import pandas as pd
from dashboard.eda_applications.src.data.loader import DataSchema
from dashboard.eda_applications.src.general_components import ids
from dash.dependencies import Input, Output



def render(app: DjangoDash, data: pd.DataFrame) -> html.Div:
    all_countries = list(data[DataSchema.COUNTRY].unique())
    @app.callback(
        Output(ids.COUNTRIES_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_COUNTRIES_BUTTON, 'n_clicks')
      
    )
    def select_all_nations(_: int) -> list[str]:
        return all_countries
    return html.Div(
        children= [
            html.H6('Country'),
            dcc.Dropdown(
                id=ids.COUNTRIES_DROPDOWN,
                options = [{'label': country, 'value': country} for country in all_countries],
                value = all_countries,
                multi=True
            ),
            html.Button(
                id=ids.SELECT_ALL_COUNTRIES_BUTTON,
                children=['All Countries']
            )
        ],
    )