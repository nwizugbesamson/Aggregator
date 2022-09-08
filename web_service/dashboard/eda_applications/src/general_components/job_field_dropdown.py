from collections.abc import Iterator
from dash import html, dcc
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import pandas as pd
from dashboard.eda_applications.src.data.loader import DataSchema, count_unique
from dashboard.eda_applications.src.general_components import ids

def render(app: DjangoDash, data: list[Iterator[pd.DataFrame]]) -> html.Div:
    """render Dash dropdown
    
    Arg:
        data (pd.DataFrame) : dataframe object
    Returns:
        dash.html.div
    """
    all_fields = count_unique(DataSchema.JOB_FIELD, data)

    @app.callback(
        Output(ids.JOB_FIELD_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_JOB_FIELDS, 'n_clicks')
    )
    def select_all_fields(_: int) -> list[str]:
        return all_fields

    return html.Div(
        children=[
            html.H6('Job Field'),
            dcc.Dropdown(
                id=ids.JOB_FIELD_DROPDOWN,
                options=[{'label': field, 'value': field} for field in all_fields],
                value=all_fields,
                multi=True
            ),
            html.Button(
                id=ids.SELECT_ALL_JOB_FIELDS,
                children=['All Job Fields']
            )
        ]
    )