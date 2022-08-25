from dash import  html, dcc
import pandas as pd
from web_service.dashboard.eda_applications.src.data.loader import DataSchema
from web_service.dashboard.eda_applications.src.personalised_components import p_ids




def render(data: pd.DataFrame) -> html.Div:
    all_fields = list(data[DataSchema.JOB_FIELD].unique())
    return html.Div(
        className= '',  # class name to apply style
        children= [
            html.H6('Job Field'),
            dcc.Dropdown(
                id=p_ids.P_JOB_FIELD_DROPDOWN,
                options = [{'label': field, 'value': field} for field in all_fields],
                value = '',
                placeholder="Select a Field",
            )
        ],
    )