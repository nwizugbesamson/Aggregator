from dash import  html, dcc
import pandas as pd
from web_service.dashboard.eda_applications.src.data.loader import DataSchema
from web_service.dashboard.eda_applications.src.personalised_components import p_ids




def render( data: pd.DataFrame) -> html.Div:
    all_countries = list(data[DataSchema.COUNTRY].unique())
    return html.Div(
        className= '',  # class name to apply style
        children= [
            html.H6('Country'),
            dcc.Dropdown(
                id=p_ids.P_COUNTRIES_DROPDOWN,
                options = [{'label': country, 'value': country} for country in all_countries],
                value = '',
                placeholder="Select a country",
            )
        ],
    )