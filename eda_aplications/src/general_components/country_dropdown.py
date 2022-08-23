from dash import Dash, html, dcc
import pandas as pd
from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids
from dash.dependencies import Input, Output
# from eda_aplications.src.resources import COUNTRIES



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_countries = list(data[DataSchema.COUNTRY].unique())
    @app.callback(
        Output(ids.COUNTRIES_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_COUNTRIES_BUTTON, 'n_clicks')
      
    )
    def select_all_nations(_: int) -> list[str]:
        return all_countries
    return html.Div(
        className= '',  # class name to apply style
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
                className="", # styling
                children=['All Countries']
            )
        ],
    )