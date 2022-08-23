from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from eda_aplications.src.data.loader import DataSchema
from eda_aplications.src.general_components import ids



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_fields = list(data[DataSchema.JOB_FIELD].unique())

    @app.callback(
        Output(ids.JOB_FIELD_DROPDOWN, 'value'),
        Input(ids.SELECT_ALL_JOB_FIELDS, 'n_clicks')
    )
    def select_all_fields(_: int) -> list[str]:
        return all_fields

    return html.Div(
        className='', # styling
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